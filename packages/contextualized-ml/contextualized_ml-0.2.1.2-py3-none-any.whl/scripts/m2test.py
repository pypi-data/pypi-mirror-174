import time
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
import pytorch_lightning as pl
import numpy as np


class MLP(nn.Module):
    """
    Multi-layer perceptron
    """
    def __init__(self, input_dim, output_dim, width, layers, activation=nn.ReLU, link_fn=lambda x: x):
        super(MLP, self).__init__()
        hidden_layers = [layer for _ in range(0, layers - 2) for layer in (nn.Linear(width, width), activation())]
        mlp_layers = [nn.Linear(input_dim, width), activation()] + hidden_layers + [nn.Linear(width, output_dim)]
        self.mlp = nn.Sequential(*mlp_layers)
        self.link_fn = link_fn

    def forward(self, x):
        return self.link_fn(self.mlp(x))


class SoftSelect(nn.Module):
    """
    Parameter sharing for multiple context encoders:
    Batched computation for mapping many subtypes onto d-dimensional archetypes
    """
    def __init__(self, in_dims, out_shape):
        super(SoftSelect, self).__init__()
        init_mat = torch.rand(list(out_shape) + list(in_dims)) * 2e-2 - 1e-2
        self.archetypes = nn.parameter.Parameter(init_mat, requires_grad=True)

    def forward(self, *batch_weights):
        batch_size = batch_weights[0].shape[0]
        expand_dims = [batch_size] + [-1 for _ in range(len(self.archetypes.shape))]
        batch_archetypes = self.archetypes.unsqueeze(0).expand(expand_dims)
        for batch_w in batch_weights[::-1]:
            batch_w = batch_w.unsqueeze(-1)
            d = len(batch_archetypes.shape) - len(batch_w.shape)
            for _ in range(d):
                batch_w = batch_w.unsqueeze(1)
            batch_archetypes = torch.matmul(batch_archetypes, batch_w).squeeze(-1)
        return batch_archetypes


class Explainer(nn.Module):
    """
    2D subtype-archetype parameter sharing
    """
    def __init__(self, k, out_shape):
        super(Explainer, self).__init__()
        self.softselect = SoftSelect((k, ), out_shape)

    def forward(self, batch_subtypes):
        return self.softselect(batch_subtypes)


class CEN(pl.LightningModule):
    def __init__(self, c_dim, x_dim, y_dim, k, learning_rate=1e-3, **kwargs):
        super().__init__()
        self.learning_rate = learning_rate
        self.mlp = MLP(c_dim, k, 10, 5, link_fn=nn.functional.softmax)
        self.explainer = Explainer(k, (y_dim, ))

    def forward(self, C):
        Z = self.mlp(C)
        beta = self.explainer(Z)
        return beta

    def _batch_loss(self, batch, batch_idx):
        C, X, Y = batch
        beta_hat = self(C)
        Y_pred = (beta_hat * X).sum(axis=-1).unsqueeze(-1)
        residual = Y - Y_pred
        return residual.pow(2).mean()

    def training_step(self, batch, batch_idx):
        loss = self._batch_loss(batch, batch_idx)
        self.log_dict({'train_loss': loss})
        return loss

    def validation_step(self, batch, batch_idx):
        loss = self._batch_loss(batch, batch_idx)
        self.log_dict({'val_loss': loss})
        return loss

    def test_step(self, batch, batch_idx):
        loss = self._batch_loss(batch, batch_idx)
        self.log_dict({'test_loss': loss})
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.learning_rate)
        return optimizer


if __name__ == '__main__':
    print('starting test')
    dataset = lambda n: (torch.rand((n, 100)), torch.rand((n, 20)), torch.rand((n, 1)))
    train_dataset = DataLoader(TensorDataset(*dataset(1000)), batch_size=1)
    val_dataset = DataLoader(TensorDataset(*dataset(100)), batch_size=1)
    
    # Warmup
    print('warmup')
    trainer = pl.Trainer(max_epochs=1, auto_lr_find=True, accelerator='cpu', devices=1)
    model = CEN(100, 20, 1, 100)
    trainer.fit(model, train_dataset, val_dataset)
    trainer.test(model, train_dataset)
    end = time.time()
    
    trainer = pl.Trainer(max_epochs=1, auto_lr_find=True, accelerator='mps', devices=1)
    model = CEN(100, 20, 1, 100)
    trainer.fit(model, train_dataset, val_dataset)
    trainer.test(model, train_dataset)
    end = time.time()

    print('testing')
    cpu_times = []
    mps_times = []
    for i in range(5):
        start = time.time()
        trainer = pl.Trainer(max_epochs=1, auto_lr_find=True, accelerator='cpu', devices=1)
        model = CEN(100, 20, 1, 100, 5)
        trainer.fit(model, train_dataset, val_dataset)
        trainer.test(model, train_dataset)
        diff = time.time() - start
        cpu_times.append(diff)
        print(f'CPU: {diff}')
        
        start = time.time()
        trainer = pl.Trainer(max_epochs=1, auto_lr_find=True, accelerator='mps', devices=1)
        model = CEN(100, 20, 1, 100, 5)
        trainer.fit(model, train_dataset, val_dataset)
        trainer.test(model, train_dataset) 
        diff = time.time() - start
        mps_times.append(diff)
        print(f'MPS: {diff}')
    
    print(f'CPU: {np.mean(cpu_times)} ({np.var(cpu_times)})')
    print(f'MPS: {np.mean(mps_times)} ({np.var(mps_times)})')
