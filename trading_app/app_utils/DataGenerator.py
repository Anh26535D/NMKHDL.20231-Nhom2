import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import time

import pandas as pd
from trading_app.app_utils import Predictor

class DataGenerators:

    def __init__(self, file_path, model_path, window_size=20, window_display_size=50, num_data_for_setup=100) -> None:
        self.file_path = file_path
        self.last_idx = 0
        self.window_size = window_size
        self.window_display_size = window_display_size
        self.predictor = Predictor.Predictor(
            model_path=model_path,
            window_size=window_size,
        )
        self.num_data_for_setup = num_data_for_setup
        self.is_running = True

    def convert_to_json(self, row):
        prediction = None
        if self.last_idx > self.window_size:
            prediction = self.predictor.predict(data=row)['action']
            if prediction == 'buy':
                prediction = 0
            elif prediction == 'sell':
                prediction = 1
            else:
                prediction = None
           
        json_data = json.dumps({
            'Date': row['Date'],
            'Close': row['Close'],
            'AdjustedPrice': row['AdjustedPrice'],
            'Change': row['Change'],
            'MatchedVolume': row['MatchedVolume'],
            'MatchedValue': row['MatchedValue'],
            'NegotiatedVolume': row['NegotiatedVolume'],
            'NegotiatedValue': row['NegotiatedValue'],
            'Open': row['Open'],
            'High': row['High'],
            'Low': row['Low'],
            'Prediction': prediction if prediction is not None else 'N/A',
        })       
        return json_data
    
    def stop(self):
        self.is_running = False

    def run(self):
        df = pd.read_csv(self.file_path)[::-1].reset_index(drop=True)
        data_setup = df.head(min(self.num_data_for_setup, df.shape[0]))
        self.predictor.setup_agent(data=data_setup)
        self.last_idx = data_setup.shape[0]
        if df.shape[0] > self.last_idx:
            for _, row in df.iloc[self.last_idx:].iterrows():
                json_data = self.convert_to_json(row)
                yield f"data:{json_data}\n\n"
                self.last_idx += 1

        while self.is_running:
            df = pd.read_csv(self.file_path)[::-1].reset_index(drop=True)
            if df.shape[0] > self.last_idx:
                for _, row in df.iloc[self.last_idx:].iterrows():
                    json_data = self.convert_to_json(row)
                    yield f"data:{json_data}\n\n"
                    self.last_idx += 1
                    time.sleep(1)
                    