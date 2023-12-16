import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime
import re

from flask import Flask, render_template, request, jsonify
import pandas as pd

from src.model_training.trainer import RandomModel

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

@app.route('/symbol_data', methods=['GET', 'POST'])
def symbol_data():
    selected_symbol = request.form.get('symbol')
    filepath = f'data/processed/prices/{selected_symbol}.csv'
    
    try:
        df = pd.read_csv(filepath)
        first_ten_rows = df.head(10).to_html(index=False)
        loaded_model = load_model()
        prediction = predict(loaded_model, df).tolist()
        return jsonify(first_ten_rows=first_ten_rows, prediction=prediction)
    except FileNotFoundError:
        return jsonify(error="Data not available for the selected symbol.")

@app.route('/')
def home():
    symbols = get_all_symbols()
    return render_template('index.html', symbols=symbols)

if __name__ == '__main__':
    app.run(debug=True)
