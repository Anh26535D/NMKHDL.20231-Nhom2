from crawler.VietStock import ListingCompanyVietStock

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

data.to_csv(f'dataset/companies.csv', index=False)