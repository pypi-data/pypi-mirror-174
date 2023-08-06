import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans


class PopulationCorrelation:
    def fit(self, C, X):
        self.p = X.shape[-1]
        self.regs = [[LinearRegression() for _ in range(self.p)] for _ in range(self.p)]
        for i in range(self.p):
            for j in range(self.p):
                self.regs[i][j].fit(X[:, j, np.newaxis], X[:, i, np.newaxis])
        return self

    def predict(self, C):
        betas = np.zeros((self.p, self.p))
        for i in range(self.p):
            for j in range(self.p):
                betas[i, j] = self.regs[i][j].coef_.squeeze()
        corrs = betas * betas.T
        return np.tile(np.expand_dims(corrs, axis=0), (len(C), 1, 1))

    def mse(self, C, X):
        mses = np.zeros((self.p, self.p))
        for i in range(self.p):
            for j in range(self.p):
                mses[i, j] = (
                    (self.regs[i][j].predict(X[:, j, np.newaxis]) - X[:, i, np.newaxis])
                    ** 2
                ).mean()
        return mses.mean()


class ClusteredCorrelation:
    def __init__(self, K, clusterer=None):
        self.K = K
        if clusterer is None:
            self.kmeans = KMeans(n_clusters=K)
            self.prefit = False
        else:
            self.kmeans = clusterer
            self.prefit = True
        self.models = {k: PopulationCorrelation() for k in range(K)}

    def fit(self, C, X):
        self.p = X.shape[-1]
        if not self.prefit:
            self.kmeans.fit(C)
        labels = self.kmeans.predict(C)
        for k in range(self.K):
            k_idx = labels == k
            X_k, C_k = X[k_idx], C[k_idx]
            self.models[k].fit(C_k, X_k)
        return self

    def predict(self, C):
        labels = self.kmeans.predict(C)
        corrs = np.zeros((len(C), self.p, self.p))
        for label in np.unique(labels):
            l_idx = labels == label
            C_l = C[l_idx]
            corrs[l_idx] = self.models[label].predict(C_l)
        return corrs

    def mse(self, C, X):
        labels = self.kmeans.predict(C)
        mse = 0
        for label in np.unique(labels):
            l_idx = labels == label
            l_count = sum(l_idx)
            C_l, X_l = C[l_idx], X[l_idx]
            mse += l_count / len(C) * self.models[label].mse(C_l, X_l)
        return mse
