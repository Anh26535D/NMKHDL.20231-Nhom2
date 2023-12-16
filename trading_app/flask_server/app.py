from flask import Flask, render_template, request
import os
import pandas as pd

app = Flask(__name__)

def get_all_symbols():
    data_folder = 'data/processed/prices'
    symbols = []

    for filename in os.listdir(data_folder):
        if filename.endswith('.csv'):
            symbol = filename[:-4]
            symbols.append(symbol)

    return symbols

@app.route('/symbol_data', methods=['GET', 'POST'])
def symbol_data():
    selected_symbol = request.form.get('symbol')
    filepath = f'data/processed/prices/{selected_symbol}.csv'
    
    try:
        df = pd.read_csv(filepath)
        first_ten_rows = df.head(10).to_html()
        return first_ten_rows
    except FileNotFoundError:
        return "Data not available for the selected symbol."

@app.route('/')
def home():
    symbols = get_all_symbols()
    return render_template('index.html', symbols=symbols)

if __name__ == '__main__':
    app.run(debug=True)
