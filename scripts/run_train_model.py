import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import datetime
import copy
import joblib

import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.preprocessing import MinMaxScaler

from src.model_training.Model import Model
from src.model_training.Agent import Agent

def get_all_symbols():
    data_folder = 'data/processed/prices'
    symbols = []

    for filename in os.listdir(data_folder):
        if filename.endswith('.csv'):
            symbol = filename[:-4]
            symbols.append(symbol)

    return symbols

def save_model(agent, save_path='model.pkl'):
    copy_model = copy.deepcopy(agent.model)
    joblib.dump(copy_model, save_path)

if __name__ == '__main__':
    print('[START >>] Train model...')
    window_size = 20
    parameters = ['Close', 'MatchedVolume']
    state_shape = len(parameters) * (window_size - 1) * 2
    input_size = state_shape + 3 # 3 is additional params (inventory, mean_inventory, capital)

    layer_size = 500
    output_size = 3

    model = Model(input_size = input_size, layer_size = layer_size, output_size = output_size)
    agent = None

    symbols = [get_all_symbols()[0]]
    for no, symbol in tqdm(enumerate(symbols)):
        print(f'Training symbol {symbol}')
        df = pd.read_csv(f'data/processed/prices/{symbol}.csv')
        real_trend = df['Close'].tolist()
        parameters = [df['Close'].tolist(), df['MatchedVolume'].tolist()]
        minmax_scaler = MinMaxScaler(feature_range = (100, 200)).fit(np.array(parameters).T)
        scaled_parameters = minmax_scaler.transform(np.array(parameters).T).T.tolist()
        initial_money = np.max(parameters[0]) * 2
        
        if no == 0:
            agent = Agent(model = model,
                        timeseries = scaled_parameters,
                        initial_money = initial_money,
                        real_trend = real_trend,
                        minmax_scaler = minmax_scaler)
        else:
            agent.change_data(timeseries = scaled_parameters,
                            initial_money = initial_money,
                            real_trend = real_trend,
                            minmax_scaler = minmax_scaler)
        
        agent.fit(iterations = 100, checkpoint = 10)

    date_now = datetime.datetime.now().strftime('%Y-%m-%d')
    save_path = 'trading_app/model/model_' + date_now + '.pkl'
    save_model(agent, save_path=save_path)

    print('[END <<] Train model...')
