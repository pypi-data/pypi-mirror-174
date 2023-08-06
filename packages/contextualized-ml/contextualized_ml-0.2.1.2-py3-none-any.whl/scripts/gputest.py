import sys

if sys.argv[1] == 'torch':
    import torch
    print(f'torch: {torch.cuda.is_available()}')
if sys.argv[1] == 'tensorflow':
    import tensorflow as tf
    print(f'tensorflow: {tf.config.list_physical_devices("GPU")}')
