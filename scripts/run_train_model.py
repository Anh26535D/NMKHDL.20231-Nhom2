import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import datetime

from src.model_training.trainer import RandomModel

if __name__ == '__main__':
    print('[START >>] Train model...')

    date_now = datetime.datetime.now().strftime('%Y-%m-%d')
    save_path = 'trading_app/model/model_' + date_now + '.pkl'
    random_model = RandomModel()
    random_model.save_model(save_path)

    print('[END <<] Train model...')
