import sys
import os
current_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_script_dir, '..', '..')))
from datetime import datetime

import numpy as np
from sklearn.preprocessing import MinMaxScaler

from src.model_training.Model import Model
from src.model_training.Trainer import Deep_Evolution_Strategy
from src.model_training.functional import softmax

class Agent:

    POPULATION_SIZE = 15
    SIGMA = 0.1
    LEARNING_RATE = 0.03

    def __init__(
            self, 
            model: Model, 
            timeseries, 
            initial_money, 
            real_trend, 
            minmax_scaler: MinMaxScaler,
            window_size = 20
        ) -> None:

        self.model = model
        self.timeseries = timeseries # Series of stock information (Close, Volumne, etc.)
        self.real_trend = real_trend # Series that is interested in (Close)
        self.initial_money = initial_money # Initial money to trade
        self.es = Deep_Evolution_Strategy(
            self.model.get_weights(),
            self.get_reward,
            self.POPULATION_SIZE,
            self.SIGMA,
            self.LEARNING_RATE,
        )
        self.minmax_scaler = minmax_scaler
        self.window_size = window_size # Number of previous data to be used for prediction
        self._initiate()

    def _initiate(self):
        self.trend = self.timeseries[0] # Assume that the first series of timeseries is Close
        self._mean = np.mean(self.trend)
        self._std = np.std(self.trend)
        self._inventory = [] # Number of stocks that are currently owned
        self._capital = self.initial_money # Current money
        self._queue = [] # Queue of previous data
        self._scaled_capital = self.minmax_scaler.transform([[self._capital, 2]])[0, 0] # Scaled current money

    def reset_capital(self, capital):
        if capital:
            self._capital = capital
        self._scaled_capital = self.minmax_scaler.transform([[self._capital, 2]])[0, 0]
        self._queue = []
        self._inventory = []     

    def trade(self, data):
        """
        Arguments
        ---------
        data: list
            data with shape of (num_features, num_timestamps), currently support num_features = 2 (close, volume)
        """
        scaled_data = self.minmax_scaler.transform([data])[0]
        real_close = data[0]
        scaled_close = scaled_data[0]
        if len(self._queue) >= self.window_size:
            self._queue.pop(0)
        self._queue.append(scaled_data)
        if len(self._queue) < self.window_size:
            return {
                'status': 'data not enough to trade',
                'action': 'fail',
                'balance': self._capital,
                'timestamp': str(datetime.now()),
            }
        state = self.get_state(
            self.window_size - 1,
            self._inventory,
            self._scaled_capital,
            timeseries = np.array(self._queue).T.tolist(),
        )
        action, prob = self.get_action_proba(state)
        if action == 1 and self._scaled_capital >= scaled_close:
            self._inventory.append(scaled_close)
            self._scaled_capital -= scaled_close
            self._capital -= real_close
            return {
                'status': 'buy 1 unit, cost %f' % (real_close),
                'action': 'buy',
                'balance': self._capital,
                'timestamp': str(datetime.now()),
            }
        elif action == 2 and len(self._inventory):
            bought_price = self._inventory.pop(0)
            self._scaled_capital += scaled_close
            self._capital += real_close
            scaled_bought_price = self.minmax_scaler.inverse_transform(
                [[bought_price, 2]]
            )[0, 0]
            try:
                invest = (
                    (real_close - scaled_bought_price) / scaled_bought_price
                ) * 100
            except:
                invest = 0
            return {
                'status': 'sell 1 unit, price %f' % (real_close),
                'investment': invest,
                'gain': real_close - scaled_bought_price,
                'balance': self._capital,
                'action': 'sell',
                'timestamp': str(datetime.now()),
            }
        else:
            return {
                'status': 'do nothing',
                'action': 'nothing',
                'balance': self._capital,
                'timestamp': str(datetime.now()),
            }

    def change_data(self, timeseries, initial_money, real_trend, minmax_scaler):
        self.timeseries = timeseries
        self.initial_money = initial_money
        self.real_trend = real_trend
        self.minmax_scaler = minmax_scaler
        self._initiate()

    def get_action_proba(self, sequence):
        decision = self.model.forward(np.array(sequence))
        return np.argmax(decision[0]), softmax(decision)[0]
    
    def feature_engineering(self, parameters, t):
        outside = []
        d = t - self.window_size + 1
        for parameter in parameters:
            block = (
                parameter[d : t + 1]
                if d >= 0
                else -d * [parameter[0]] + parameter[0 : t + 1]
            )
            res = []
            for i in range(self.window_size - 1):
                res.append(block[i + 1] - block[i])
            for i in range(1, self.window_size, 1):
                res.append(block[i] - block[0])
            outside.append(res)
        return np.array(outside).reshape((1, -1))

    def get_state(self, t, inventory, capital, timeseries):
        state = self.feature_engineering(timeseries, t)
        len_inventory = len(inventory)
        if len_inventory:
            mean_inventory = np.mean(inventory)
        else:
            mean_inventory = 0
        z_inventory = (mean_inventory - self._mean) / self._std
        z_capital = (capital - self._mean) / self._std
        concat_parameters = np.concatenate(
            [state, [[len_inventory, z_inventory, z_capital]]], axis = 1
        )
        return concat_parameters

    def get_reward(self, weights):
        self.model.weights = weights
        initial_money = self._scaled_capital
        starting_money = initial_money
        invests = []
        inventory = []
        state = self.get_state(0, inventory, starting_money, self.timeseries)

        for t in range(0, len(self.trend) - 1):
            action, proba = self.get_action_proba(state)
            if action == 1 and starting_money >= self.trend[t]:
                inventory.append(self.trend[t])
                starting_money -= self.trend[t]
            elif action == 2 and len(inventory):
                bought_price = inventory.pop(0)
                starting_money += self.trend[t]
                invest = ((self.trend[t] - bought_price) / bought_price) * 100
                invests.append(invest)

            state = self.get_state(
                t + 1, inventory, starting_money, self.timeseries
            )
        if invests:
            mean_invests = np.mean(invests)
        if np.isnan(mean_invests):
            mean_invests = 0
        score = (starting_money - initial_money) / initial_money * 100
        return mean_invests * 0.7 + score * 0.3

    def fit(self, iterations, checkpoint):
        self.es.train(iterations, print_every=checkpoint)