import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from tqdm import tqdm

from src.data_processing.crawler import CafeF

LIST_COMPANIES_PATH = 'data/raw/companies.csv'
START_DATE = '01/01/2015'
END_DATE = '01/01/2021'
PRICES_PATH = 'data/raw/prices'

if __name__ == '__main__':
    print('[START >>] Crawling prices...')
    companies = pd.read_csv(LIST_COMPANIES_PATH)
    symbols = companies['symbol'].values

    crawler = CafeF.HistoricalPriceCafef()
    for symbol in tqdm(symbols, total=len(symbols)):
        data = crawler.getHistoricalPrice(
            symbol,
            start_date=START_DATE,
            end_date=END_DATE,
        )
        data.to_csv(os.path.join(PRICES_PATH, f'{symbol}.csv'), index=False)

    print('[END <<] Crawling prices...')