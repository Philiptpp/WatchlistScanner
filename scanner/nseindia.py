import datetime

import pandas as pd
from bs4 import BeautifulSoup as bs

import requests
import quandl


__token__ = "Eunmnd2xhzFovbzo3uKz"


def get_historical_price(scrip, start=None, end=None):
    try:
        df = quandl.get('NSE/{}'.format(scrip), authtoken=__token__)
    except:
        print('\nUnknown scrip {}\n'.format(scrip))
    df['Symbol'] = scrip
    df['Date'] = df.index
    df.reset_index(drop=True, inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date', inplace=True)
    df.rename({'Symbol': 'symbol',
        'Date': 'date',
        'Open': 'open',
        'Close': 'close',
        'High': 'high',
        'Low': 'low',
        'Total Trade Quantity': 'volume'}, axis=1, inplace=True)
    for col in ['open','close','high','low']:
        df[col] = df[col].astype(float)
    df['volume'].fillna(value=0, inplace=True)
    df['volume'] = df['volume'].astype(int)
    return df
