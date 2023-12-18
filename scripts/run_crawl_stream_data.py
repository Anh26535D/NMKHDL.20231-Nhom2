import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
from src.data_processing.crawler import CafeF
from src.data_processing.transformer import NameTransformer
from src.data_processing import transformer
from datetime import datetime, timedelta
PROCESSED_PATH = 'data/processed/prices'

if __name__ == '__main__':
    if (len(sys.argv) > 2):
        symbol = sys.argv[1]
        period = int(sys.argv[2])
        
        csv_file_path = os.path.join(PROCESSED_PATH,f'{symbol}.csv')

        with open(csv_file_path, 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader, None)
            first_row = next(csv_reader, None)
            start_date = first_row[0]

        start_date = (datetime.strptime(start_date, '%d/%m/%Y')+timedelta(days=1)).strftime('%m/%d/%Y')
        end_date = (datetime.strptime(start_date, '%m/%d/%Y') +
                    timedelta(days=period)).strftime('%m/%d/%Y')

        crawler = CafeF.HistoricalPriceCafef()
        data = crawler.getHistoricalPrice(
            symbol,
            start_date=start_date,
            end_date=end_date
        )
        transformer = NameTransformer.NameTransformer()
        processed_data = transformer.transform(data)
        datas = processed_data.values.tolist()
        for row in datas[::-1]:
            print(row)
            with open(csv_file_path, 'r', newline='') as csv_file:
                existing_content = csv_file.read()
            with open(csv_file_path, 'w', newline='') as csv_file:
                lines = existing_content.splitlines()
                modified_existing_content= '\n'.join(lines[1:])
                csv_writer = csv.writer(csv_file)
                csv_file.write(lines[0]+'\n')
                csv_writer.writerow(row)
                csv_file.write(modified_existing_content)

            time.sleep(1)