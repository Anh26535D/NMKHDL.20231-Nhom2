import numpy as np
import joblib

class RandomModel:
    def __init__(self):
        pass

    def train(self, data):
        pass

    def predict(self, X):
        return np.random.randint(0, 2, size=(len(X), 1))
    
    def save_model(self, save_path):
        joblib.dump(self, save_path)

    @classmethod
    def load_model(cls, load_path):
        return joblib.load(load_path)
