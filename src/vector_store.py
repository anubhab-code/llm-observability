import faiss
import numpy as np
from embedding_utils import get_embedding

class VectorStore:
    def __init__(self, dim=128):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.data = []
        self.labels = []

    def add(self, prompt, label):
        embedding = get_embedding(prompt, self.dim)
        self.index.add(np.array([embedding]).astype('float32'))
        self.data.append(prompt)
        self.labels.append(label)

    def search(self, prompt, k=1):
        if len(self.data) == 0:
            return None, 0.0
        embedding = get_embedding(prompt, self.dim)
        D, I = self.index.search(np.array([embedding]).astype('float32'), k)
        idx = I[0][0]
        sim = 1 / (1 + D[0][0])
        return self.labels[idx], sim
