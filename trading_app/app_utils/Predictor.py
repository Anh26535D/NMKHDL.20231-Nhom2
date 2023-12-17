import sys
import os
current_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_script_dir, '..', '..')))
import joblib

import numpy as np
from sklearn.preprocessing import MinMaxScaler

from src.model_training.Agent import Agent

class Predictor:

    def __init__(
            self, 
            model_path,
            window_size = 20,
        ) -> None:
        self.model = joblib.load(model_path)
        self.window_size = window_size

    def get_scaler(self, data):
        return MinMaxScaler(feature_range = (100, 200)).fit(data)
    
    def process_data(self, data):
        real_trend = data['Close'].tolist()
        volume = data['MatchedVolume'].tolist()
        parameters = [real_trend, volume]
        np_parameters = np.array(parameters).T
        self.scaler = self.get_scaler(np_parameters)
        scaled_parameters = self.scaler.transform(np_parameters).T.tolist()
        return scaled_parameters, real_trend, volume
    
    def setup_agent(self, data):
        scaled_parameters, real_trend, volume = self.process_data(data)
        initial_money = np.max(real_trend) * 2

        self.agent = Agent(
            model=self.model,
            timeseries = scaled_parameters,
            initial_money = initial_money,
            real_trend = scaled_parameters[0],
            minmax_scaler = self.scaler
        )
    
    def predict(self, data):
        """Predict the next action based on the data (Close, Volume)"""
        return self.agent.trade([data['Close'],  data['MatchedVolume']])