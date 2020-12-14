import requests
import pandas as pd
import json
import time
import os


def company_info(ticker):
    r = requests.get(f'https://finnhub.io/api/v1/stock/profile2?symbol={ticker}&token=bv6ihlv48v6s9eue1r60').json()
    df = pd.DataFrame({'0': r})
    return df.T


full_frame = []

with open('../input/nasdaq_tickers.txt', 'r') as f:
    file = f.readlines()
    count = 0
    total = 0
    all_companies = len(file)

    clear = lambda: os.system('cls' if os.name=='nt' else 'clear')

    for company in file:
        count += 1
        total += 1
        if count == 60:
            clear()
            print(f'ETA: {((all_companies+((all_companies//60)*20)-total))//60}min')
            print('Waiting 60 seconds...')
            print(f'{total}/{all_companies} entries appended to dataframe.')
            time.sleep(60)
            count = 0
        clear()
        print(f'ETA: {((all_companies+((all_companies//60)*20)-total))//60}min')
        print('Appending to dataframe...')
        print(f'{total}/{all_companies} entries appended to dataframe.')
        data = company.split('|')
        ticker = data[0]
        full_frame.append(company_info(ticker))

mega_full_frame = pd.concat(full_frame, ignore_index=True)
mega_full_frame.to_csv('../output/all_company_data.csv')
