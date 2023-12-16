import json
import time

import pandas as pd

class DataGenerators:

    def __init__(self, filepath) -> None:
        self.filepath = filepath
        self.last_idx = 0

    def run(self):
        df = pd.read_csv(self.filepath)
        if df.shape[0] > self.last_idx:
            for _, row in df[::-1].iloc[self.last_idx:].iterrows():
                json_data = json.dumps({
                    'Date': str(row['Date']),
                    'Close': float(row['Close']),
                })
                yield f"data:{json_data}\n\n"
                self.last_idx += 1
                   
        while True:
            df = pd.read_csv(self.filepath)

            if df.shape[0] > self.last_idx:
                for _, row in df[::-1].iloc[self.last_idx:].iterrows():
                    json_data = json.dumps({
                        'Date': str(row['Date']),
                        'Close': float(row['Close']),
                    })
                    yield f"data:{json_data}\n\n"
                    self.last_idx += 1
                    time.sleep(0.5)
                    