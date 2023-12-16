import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_processing.crawler.VietStock import ListingCompanyVietStock

if __name__ == '__main__':
    print('[START >>] Crawling listing...')
    crawler = ListingCompanyVietStock()
    data = crawler.run()
    data.set_index('STT', inplace=True)
    data.rename(columns={
        'Mã CK▲': 'symbol',
        'Tên công ty': 'company',
        'Ngành': 'industry',
        'Sàn': 'exchange',
        'Khối lượng NY/ĐKGD': 'trading_volume_and_chartered_capital'
    }, inplace=True)

    data.to_csv(f'data/raw/companies.csv', index=False)
    print('[END <<] Crawling listing...')
