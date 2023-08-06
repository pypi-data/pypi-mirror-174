import torch
import numpy as np
from contextualized.regression.lightning_modules import ContextualizedCorrelation
from contextualized.regression.trainers import CorrelationTrainer
from contextualized.regression import LINK_FUNCTIONS


C_train = np.random.normal(0, 1, (1000, 20))
X_train = np.random.normal(0, 1, (1000, 5))
subtype_kwargs = {
    'num_archetypes': 10, 
    'encoder_type': 'mlp',
    'encoder_kwargs': {'width': 25, 'layers': 3, 'link_fn': LINK_FUNCTIONS['identity']},
}
correlator = ContextualizedCorrelation(
    C_train.shape[-1], 
    X_train.shape[-1], 
    **subtype_kwargs
)
train_dataset = correlator.dataloader(C_train, X_train, batch_size=1)
trainer = CorrelationTrainer(max_epochs=20, auto_lr_find=True, accelerator='cpu', devices=1)
trainer.fit(correlator, train_dataset)

correlator = ContextualizedCorrelation(
    C_train.shape[-1], 
    X_train.shape[-1], 
    **subtype_kwargs
)
train_dataset = correlator.dataloader(C_train, X_train, batch_size=1)
trainer = CorrelationTrainer(max_epochs=20, auto_lr_find=True, accelerator='mps', devices=1)
trainer.fit(correlator, train_dataset)
