import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import logging
logging.basicConfig(
    filename='datalogs/empty_symbols.ini', 
    filemode='w',
    level=logging.ERROR, 
    encoding='utf-8'
)

import pandas as pd
from tqdm import tqdm
from src.data_processing.transformer import NameTransformer

RAW_PATH = 'data/raw/prices'
PROCESSED_PATH = 'data/processed/prices'

if __name__ == '__main__':
    print('[START >>] Transforming prices...')
    filenames = os.listdir(RAW_PATH)
    transformer = NameTransformer.NameTransformer()
    for filename in tqdm(filenames, total=len(filenames)):
        try:
            data = pd.read_csv(os.path.join(RAW_PATH, filename))
            processed_data = transformer.transform(data)
            processed_data.to_csv(os.path.join(PROCESSED_PATH, filename), index=False)
        except pd.errors.EmptyDataError:
            logging.error(f'{filename}')
    print('[END <<] Transforming prices...')
