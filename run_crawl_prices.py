import pandas as pd
from tqdm import tqdm
import os

from crawler.CafeF import HistoricalPriceCafef

LIST_COMPANIES_PATH = 'dataset/companies.csv'
START_DATE = '01/01/2015'
END_DATE = '01/01/2021'
PRICES_PATH = 'dataset/prices'

companies = pd.read_csv(LIST_COMPANIES_PATH)
symbols = companies['symbol'].values

crawler = HistoricalPriceCafef()
for symbol in tqdm(symbols, total=len(symbols)):
    data = crawler.getHistoricalPrice(
        symbol,
        start_date=START_DATE,
        end_date=END_DATE,
    )
    data.to_csv(os.path.join(PRICES_PATH, f'{symbol}.csv'), index=False)

print('Done!')