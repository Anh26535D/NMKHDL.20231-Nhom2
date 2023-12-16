import json
import time

import pandas as pd

class DataGenerators:

    def __init__(self, filepath) -> None:
        self.filepath = filepath
        self.last_idx = 0

    def run(self):
        df = pd.read_csv(self.filepath)
        df = df[::-1]

        if df.shape[0] > self.last_idx:
            for _, row in df.iloc[self.last_idx:].iterrows():
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
                })
                yield f"data:{json_data}\n\n"
                self.last_idx += 1
                   
        while True:
            df = pd.read_csv(self.filepath)
            df = df[::-1]

            if df.shape[0] > self.last_idx:
                for _, row in df.iloc[self.last_idx:].iterrows():
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
                    })
                    yield f"data:{json_data}\n\n"
                    self.last_idx += 1
                    time.sleep(0.5)
                    