import numpy as np

def get_embedding(text, dim=128):
    np.random.seed(abs(hash(text)) % (10**6))
    return np.random.rand(dim)
