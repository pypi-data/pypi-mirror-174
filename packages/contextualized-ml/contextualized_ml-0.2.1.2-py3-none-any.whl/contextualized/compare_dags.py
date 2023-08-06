"""
Unit tests for DAG models.
"""
import unittest
import numpy as np
import igraph as ig

from contextualized.dags.lightning_modules import NOTMAD
from contextualized.dags import graph_utils
from contextualized.dags.trainers import GraphTrainer

from contextualized.dags_old.torch_notmad import NOTMAD_model
from contextualized.dags_old.datamodules import CXW_DataModule
from contextualized.dags_old.callbacks import DynamicAlphaRho
from pytorch_lightning import Trainer

from pytorch_lightning.utilities.seed import seed_everything


def simulate_linear_sem(W, n, sem_type, noise_scale=None):
    """Simulate samples from linear SEM with specified type of noise.

    For uniform, noise z ~ uniform(-a, a), where a = noise_scale.

    Args:
        W (np.ndarray): [d, d] weighted adj matrix of DAG
        n (int): num of samples, n=inf mimics population risk
        sem_type (str): gauss, exp, gumbel, uniform, logistic, poisson
        noise_scale (np.ndarray): scale parameter of additive noise, default all ones

    Returns:
        X (np.ndarray): [n, d] sample matrix, [d, d] if n=inf
    """

    def _simulate_single_equation(X, w, scale):
        """X: [n, num of parents], w: [num of parents], x: [n]"""
        if sem_type == "gauss":
            z = np.random.normal(scale=scale, size=n)
            # x = X @ w + z
            x = np.matmul(X, w) + z
        elif sem_type == "exp":
            z = np.random.exponential(scale=scale, size=n)
            # x = X @ w + z
            x = np.matmul(X, w) + z
        elif sem_type == "gumbel":
            z = np.random.gumbel(scale=scale, size=n)
            # x = X @ w + z
            x = np.matmul(X, w) + z
        elif sem_type == "uniform":
            z = np.random.uniform(low=-scale, high=scale, size=n)
            # x = X @ w + z
            x = np.matmul(X, w) + z
        elif sem_type == "logistic":
            # x = np.random.binomial(1, sigmoid(X @ w)) * 1.0
            x = np.random.binomial(1, sigmoid(np.matmul(X, w))) * 1.0
        elif sem_type == "poisson":
            # x = np.random.poisson(np.exp(X @ w)) * 1.0
            x = np.random.poisson(np.exp(np.matmul(X, w))) * 1.0
        else:
            raise ValueError("unknown sem type")
        return x

    d = W.shape[0]
    if noise_scale is None:
        scale_vec = np.ones(d)
    elif np.isscalar(noise_scale):
        scale_vec = noise_scale * np.ones(d)
    else:
        if len(noise_scale) != d:
            raise ValueError("noise scale must be a scalar or has length d")
        scale_vec = noise_scale
    if not graph_utils.is_dag(W):
        raise ValueError("W must be a DAG")
    if np.isinf(n):  # population risk for linear gauss SEM
        if sem_type == "gauss":
            # make 1/d X'X = true cov
            # X = np.sqrt(d) * np.diag(scale_vec) @ np.linalg.inv(np.eye(d) - W)
            X = np.sqrt(d) * np.matmul(np.diag(scale_vec), np.linalg.inv(np.eye(d) - W))
            return X
        else:
            raise ValueError("population risk not available")
    # empirical risk
    G = ig.Graph.Weighted_Adjacency(W.tolist())
    ordered_vertices = G.topological_sorting()
    assert len(ordered_vertices) == d
    X = np.zeros([n, d])
    for j in ordered_vertices:
        parents = G.neighbors(j, mode=ig.IN)
        X[:, j] = _simulate_single_equation(X[:, parents], W[parents, j], scale_vec[j])
    return X


class TestNOTMAD(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestNOTMAD, self).__init__(*args, **kwargs)

    def setUp(self):
        (
            self.C,
            self.X,
            self.W,
            self.train_idx,
            self.test_idx,
            self.val_idx,
        ) = self._create_cwx_dataset()

    def _create_cwx_dataset(self, n=500):
        np.random.seed(0)
        C = np.linspace(1, 2, n).reshape((n, 1))
        blank = np.zeros_like(C)
        W_00 = blank
        W_01 = C - 2
        W_02 = blank
        W_03 = blank
        W_10 = blank
        W_11 = blank
        W_12 = blank
        W_13 = blank
        W_20 = blank
        W_21 = C**2
        W_22 = blank
        W_23 = blank
        W_30 = blank
        W_31 = C**3
        W_32 = C
        W_33 = blank

        W = np.array(
            [
                [W_00, W_01, W_02, W_03],
                [W_10, W_11, W_12, W_13],
                [W_20, W_21, W_22, W_23],
                [W_30, W_31, W_32, W_33],
            ]
        ).squeeze()

        W = np.transpose(W, (2, 0, 1))
        X = np.zeros((n, 4))
        for i, w in enumerate(W):
            x = simulate_linear_sem(w, 1, "uniform", noise_scale=0.1)[0]
            X[i] = x
        train_idx = np.logical_or(C < 1.7, C >= 1.9)[:, 0]
        test_idx = np.logical_and(C >= 1.8, C < 1.9)[:, 0]
        val_idx = np.logical_and(C >= 1.7, C < 1.8)[:, 0]
        return (
            C,
            X,
            W,
            train_idx,
            test_idx,
            val_idx,
        )

    def _quicktest(self, model, n_epochs=10):
        print(f"\n{type(model)} quicktest")

        trainer = GraphTrainer(max_epochs=n_epochs)
        C_train, C_test, C_val = (
            self.C[self.train_idx],
            self.C[self.test_idx],
            self.C[self.val_idx],
        )
        X_train, X_test, X_val = (
            self.X[self.train_idx],
            self.X[self.test_idx],
            self.X[self.val_idx],
        )
        W_train, W_test, W_val = (
            self.W[self.train_idx],
            self.W[self.test_idx],
            self.W[self.val_idx],
        )
        train_dataloader = model.dataloader(C_train, X_train, batch_size=1)
        test_dataloader = model.dataloader(C_test, X_test, batch_size=10)
        val_dataloader = model.dataloader(C_val, X_val, batch_size=10)
        trainer.tune(model, train_dataloader)
        trainer.fit(model, train_dataloader, val_dataloader)
        trainer.validate(model, val_dataloader)
        trainer.test(model, test_dataloader)
        train_preds = trainer.predict_params(
            model, train_dataloader, project_to_dag=True
        )
        test_preds = trainer.predict_params(model, test_dataloader, project_to_dag=True)
        val_preds = trainer.predict_params(model, val_dataloader, project_to_dag=True)

        mse = lambda true, pred: ((true - pred) ** 2).mean()
        print(f"train L2: {mse(train_preds, W_train)}")
        print(f"test L2:  {mse(test_preds, W_test)}")
        print(f"val L2:   {mse(val_preds, W_val)}")
        print(
            f"train mse: {mse(graph_utils.dag_pred_np(X_train, train_preds), X_train)}"
        )
        print(f"test mse:  {mse(graph_utils.dag_pred_np(X_test, test_preds), X_test)}")
        print(f"val mse:   {mse(graph_utils.dag_pred_np(X_val, val_preds), X_val)}")
        print(train_preds[0])
        print(W_train[0])
        print(train_preds[-1])
        print(W_train[-1])

    def _quicktest_old(self, model, datamodule, n_epochs=10):
        trainer = Trainer(max_epochs=n_epochs, callbacks=[])

        trainer.tune(model)
        trainer.fit(model, datamodule)
        trainer.validate(model, datamodule)
        trainer.test(model, datamodule)
        # data
        C_train = trainer.model.datamodule.C_train
        C_test = trainer.model.datamodule.C_test
        W_train = trainer.model.datamodule.W_train
        W_test = trainer.model.datamodule.W_test
        X_train = trainer.model.datamodule.X_train
        X_test = trainer.model.datamodule.X_test

        # Evaluate results
        torch_notmad_preds_train = trainer.model.predict_w(
            C_train, confirm_project_to_dag=True
        )
        torch_notmad_preds = trainer.model.predict_w(C_test).squeeze().detach().numpy()

        torch_notmad_preds_train = trainer.model.predict_w(
            C_train, confirm_project_to_dag=True
        )
        torch_notmad_preds = trainer.model.predict_w(C_test).squeeze().detach().numpy()

        mse = lambda true, pred: ((true - pred) ** 2).mean()
        dag_pred = lambda x, w: np.matmul(x, w).squeeze()
        dags_pred = lambda xs, w: [dag_pred(x, w) for x in xs]

        example_preds = dags_pred(X_train, torch_notmad_preds_train)
        actual_preds = dags_pred(X_train, W_train)

        print(f"train L2: {mse(torch_notmad_preds_train, W_train)}")
        print(f"test L2:  {mse(torch_notmad_preds, W_test)}")
        print(
            f"train mse: {mse(graph_utils.dag_pred_np(X_train, torch_notmad_preds_train), X_train)}"
        )
        print(
            f"test mse:  {mse(graph_utils.dag_pred_np(X_test, torch_notmad_preds), X_test)}"
        )
        print(torch_notmad_preds_train[0])
        print(W_train[0])
        print(torch_notmad_preds_train[-1])
        print(W_train[-1])

    def test_notmad(self):
        # 1 archetype
        # seed_everything(0)
        # k = 5
        # INIT_MAT = np.random.uniform(-0.01, 0.01, size=(k, 4, 4))
        # model = NOTMAD(
        #     self.C.shape[-1],
        #     self.X.shape[-1],
        #     init_mat=INIT_MAT,
        #     num_archetypes=k,
        # )
        # self._quicktest(model)

        seed_everything(0)
        # 10 archetypes
        k = 6
        INIT_MAT = np.random.uniform(-0.01, 0.01, size=(k, 4, 4))
        model = NOTMAD(
            self.C.shape[-1],
            self.X.shape[-1],
            init_mat=INIT_MAT,
            num_archetypes=k,
        )
        self._quicktest(model)

    def test_notmad_old(self):
        # seed_everything(0)
        # # 5 archetypes
        # k = 5
        # INIT_MAT = np.random.uniform(-0.01, 0.01, size=(k, 4, 4))
        # datamodule = CXW_DataModule(self.C, self.X, self.W, self.train_idx, self.test_idx, self.val_idx)
        # model = NOTMAD_model(
        #     datamodule,
        #     init_mat=INIT_MAT,
        #     n_archetypes=k,
        # )
        # self._quicktest_old(model, datamodule)

        seed_everything(0)
        # 6 archetypes
        k = 6
        INIT_MAT = np.random.uniform(-0.01, 0.01, size=(k, 4, 4))
        datamodule = CXW_DataModule(
            self.C, self.X, self.W, self.train_idx, self.test_idx, self.val_idx
        )
        model = NOTMAD_model(
            datamodule,
            init_mat=INIT_MAT,
            n_archetypes=k,
        )
        self._quicktest_old(model, datamodule)

    # def compare_dags(selfs):
    #     # Old NOTMAD
    #     seed_everything(0)
    #     k = 6
    #     INIT_MAT = np.random.uniform(-0.01, 0.01, size=(k, 4, 4))
    #     datamodule = CXW_DataModule(self.C, self.X, self.W, self.train_idx, self.test_idx, self.val_idx)
    #     model = NOTMAD_model(
    #         datamodule,
    #         init_mat=INIT_MAT,
    #         n_archetypes=k,
    #     )
    #
    #     seed_everything(0)
    #     k = 6
    #     INIT_MAT = np.random.uniform(-0.01, 0.01, size=(k, 4, 4))
    #     seed_everything(0)
    #     # 10 archetypes
    #     model = NOTMAD(
    #         self.C.shape[-1],
    #         self.X.shape[-1],
    #         init_mat=INIT_MAT,
    #         num_archetypes=k,
    #     )
    #     # New NOTMAD


if __name__ == "__main__":
    unittest.main()
