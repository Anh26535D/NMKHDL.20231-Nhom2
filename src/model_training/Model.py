import sys
import os
current_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_script_dir, '..', '..')))

import numpy as np

class Model:
    def __init__(self, input_size, layer_size, output_size):
        self.weights = [
            np.random.rand(input_size, layer_size) * np.sqrt(1 / (input_size + layer_size)), # W1 - (input_size, layer_size)
            np.random.rand(layer_size, output_size) * np.sqrt(1 / (layer_size + output_size)), # W2 - (layer_size, output_size)
            np.zeros((1, layer_size)), # b1 - (1, layer_size)
            np.zeros((1, output_size)), # b2 - (1, output_size)
        ]

    def forward(self, inputs):
        feed = np.dot(inputs, self.weights[0]) + self.weights[-2]
        decision = np.dot(feed, self.weights[1]) + self.weights[-1]
        return decision

    def get_weights(self):
        return self.weights

    def set_weights(self, weights):
        self.weights = weights