import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime

from flask import Flask, render_template, Response, stream_with_context

from src.model_training.trainer import RandomModel
from trading_app.app_utils import DataGenerator

app = Flask(__name__)

def get_all_symbols():
    data_folder = 'data/processed/prices'
    symbols = []

    for filename in os.listdir(data_folder):
        if filename.endswith('.csv'):
            symbol = filename[:-4]
            symbols.append(symbol)

    return symbols

def get_latest_model_path(root_path):
    model_files = os.listdir(root_path)
    model_files = [f for f in model_files if f.startswith('model_') and f.endswith('.pkl')]

    if not model_files:
        return None

    dates = [model.split('_')[1][:-4] for model in model_files]
    date_objects = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
    latest_index = date_objects.index(max(date_objects))
    latest_model_path = os.path.join(root_path, model_files[latest_index])

    return latest_model_path

def load_model():
    model_path = get_latest_model_path(root_path='trading_app/model')
    loaded_model = RandomModel.load_model(model_path)
    return loaded_model

def predict(model, data):
    prediction = model.predict(data)
    return prediction

@app.route('/chart-data/<symbol>')
def chart_data(symbol):
    filepath = f'data/processed/prices/{symbol}.csv'
    gendata = DataGenerator.DataGenerators(filepath)
    response = Response(stream_with_context(gendata.run()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

@app.route('/')
def home():
    symbols = get_all_symbols()
    return render_template('index.html', symbols=symbols)

if __name__ == '__main__':
    app.run(debug=True)
