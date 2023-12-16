import numpy as np

class Trainer:
    def __init__(self):
        print("Trainer initialized")

class RandomModel:
    def __init__(self) -> None:
        pass

    def predict(self, X):
        return np.random.randint(0, 2, size=(len(X), 1))