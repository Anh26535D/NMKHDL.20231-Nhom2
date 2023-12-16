import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import time

import pandas as pd
from trading_app.app_utils import Predictor

class DataGenerators:

    def __init__(self, file_path, model_path, window_size=10) -> None:
        self.file_path = file_path
        self.last_idx = 0
        self.window_size = window_size
        self.predictor = Predictor.Predictor(
            model_path=model_path,
            window_size=window_size,
        )

    def convert_to_json(self, row, df):
        prediction = None
        if self.last_idx > self.window_size:
            data = df.iloc[self.last_idx - self.window_size:self.last_idx].values
            prediction = self.predictor.predict(data=data)
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

    def run(self):
        df = pd.read_csv(self.file_path)
        df = df[::-1]

        if df.shape[0] > self.last_idx:
            for _, row in df.iloc[self.last_idx:].iterrows():
                json_data = self.convert_to_json(row, df)
                yield f"data:{json_data}\n\n"
                self.last_idx += 1
                   
        while True:
            df = pd.read_csv(self.file_path)
            df = df[::-1]

            if df.shape[0] > self.last_idx:
                for _, row in df.iloc[self.last_idx:].iterrows():
                    json_data = self.convert_to_json(row, df)
                    yield f"data:{json_data}\n\n"
                    self.last_idx += 1
                    time.sleep(0.5)
                    