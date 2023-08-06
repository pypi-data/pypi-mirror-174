from contextualized.regression.lightning_modules import ContextualizedCorrelation
from contextualized.regression.trainers import CorrelationTrainer
import time
import torch
import numpy as np

n, c_dim, x_dim = 1000, 100, 20
C = np.random.uniform(-1, 1, (n, c_dim))
X = np.random.uniform(-1, 1, (n, x_dim))

model = ContextualizedCorrelation(c_dim, x_dim, encoder_type="ngam")
dataset = model.dataloader(C, X, batch_size=10)
trainer = CorrelationTrainer(max_epochs=1)
start = time.time()
trainer.fit(model, dataset)
end = time.time()
print(f"warmup time: {end - start}")

model = ContextualizedCorrelation(c_dim, x_dim, encoder_type="ngam")
dataset = model.dataloader(C, X, batch_size=10)
trainer = CorrelationTrainer(max_epochs=1)
start = time.time()
trainer.fit(model, dataset)
end = time.time()
print(f"ngam time: {end - start}")


model = ContextualizedCorrelation(c_dim, x_dim, encoder_type="mlp")
dataset = model.dataloader(C, X, batch_size=10)
trainer = CorrelationTrainer(max_epochs=1)
start = time.time()
trainer.fit(model, dataset)
end = time.time()
print(f"mlp time: {end - start}")
