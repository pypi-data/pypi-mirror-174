import torch
from contextualized.networks import CorrTrainer, ContextualizedCorrelation
from contextualized.regression import *

n = 100
c_dim = 4
x_dim = 2
y_dim = 3
C = torch.rand((n, c_dim)) - .5 
W_1 = C.sum(axis=1).unsqueeze(-1) ** 2
W_2 = - C.sum(axis=1).unsqueeze(-1)
b_1 = C[:, 0].unsqueeze(-1)
b_2 = C[:, 1].unsqueeze(-1)
W_full = torch.cat((W_1, W_2), axis=1)
b_full = b_1 + b_2
X = torch.rand((n, x_dim)) - .5
Y_1 = X[:, 0].unsqueeze(-1) * W_1 + b_1
Y_2 = X[:, 1].unsqueeze(-1) * W_2 + b_2
Y_3 = X.sum(axis=1).unsqueeze(-1)
Y = torch.cat((Y_1, Y_2, Y_3), axis=1)

k = 10
epochs = 2
batch_size = 1
C, X, Y = C.numpy(), X.numpy(), Y.numpy()


def quicktest(model):
    dataloader = model.dataloader(C, X, Y, batch_size=32)
    trainer = CRTrainer(max_epochs=1)
    trainer.fit(model, dataloader)
    trainer.validate(model, dataloader)
    trainer.test(model, dataloader)
    beta_preds, mu_preds = trainer.predict_params(model, dataloader)
    y_preds = trainer.predict_y(model, dataloader)


# Naive Multivariate
model = NaiveContextualizedRegression(c_dim, x_dim, y_dim)
quicktest(model)

# Subtype Multivariate
model = SubtypeContextualizedRegression(c_dim, x_dim, y_dim)
quicktest(model)

# Multitask Multivariate
model = MultitaskContextualizedRegression(c_dim, x_dim, y_dim)
quicktest(model)

# Tasksplit Multivariate
model = TasksplitContextualizedRegression(c_dim, x_dim, y_dim)
quicktest(model)

# Tasksplit Univariate
model = TasksplitContextualizedRegression(c_dim, x_dim, y_dim)
quicktest(model)

# Correlation
model = ContextualizedCorrelation(c_dim, x_dim)
dataloader = model.dataloader(C, X, batch_size=32)
trainer = CorrTrainer(max_epochs=1)
trainer.fit(model, dataloader)
trainer.validate(model, dataloader)
trainer.test(model, dataloader)
beta_preds, mu_preds = trainer.predict_params(model, dataloader)
y_preds = trainer.predict_y(model, dataloader)
rhos = trainer.predict_network(model, dataloader)
