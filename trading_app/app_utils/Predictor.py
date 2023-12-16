import sys
import os
current_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_script_dir, '..', '..')))

import os

from src.model_training.trainer import RandomModel

class Predictor:
    def __init__(self, model_path, window_size=30) -> None:
        self.model_path = model_path
        self.window_size = window_size
        self.model = self.load_model()

    def load_model(self):
        loaded_model = RandomModel.load_model(self.model_path)
        return loaded_model

    def predict(self, data):
        prediction = self.model.predict(data)
        return prediction