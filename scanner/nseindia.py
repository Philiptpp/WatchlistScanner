import datetime

import pandas as pd
from bs4 import BeautifulSoup as bs

import requests


__url_dictionary__ = {
    'equity': 'https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol={symbol}&segmentLink=3&symbolCount={count}&series=EQ&dateRange=+&fromDate={from_dd_mm_yyyy}&toDate={to_dd_mm_yyyy}&dataType=PRICEVOLUMEDELIVERABLE',
    'symbol_count': 'https://www.nseindia.com/marketinfo/sym_map/symbolCount.jsp?symbol=INFY'
}

__headers__ = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'www.nseindia.com',
    'Referer': 'https://www.nseindia.com/products/content/equities/indices/historical_index_data.htm',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

__index__ = {"NIFTY": "NIFTY 50", "NIFTYMID50": "NIFTY MIDCAP 50", "BANKNIFTY": "NIFTY BANK", "NIFTYINFRA": "NIFTY INFRA", "NIFTYIT": "NIFTY IT", "NIFTYPSE": "NIFTY PSE", "NIFTYCPSE": "NIFTY CPSE"}
__session__ = requests.Session()
__session__.headers.update(__headers__)


def __get__(url):
    """ Returns a HTTP GET request from the url """
    res = __session__.get(url)
    if 200 <= res.status_code < 300:
        return (True, res.text)
    else:
        return (False, '')


def get_historical_price(scrip, start=None, end=None):
    status, res = __get__(__url_dictionary__.get('symbol_count'))
    count = int(res) if status else 1
    url = __url_dictionary__.get('equity')

    data = []
    to_date = datetime.datetime.today() if end is None else end
    if start is None:
        start = to_date - datetime.timedelta(days=365)
    while True:
        from_date = max(start, to_date - datetime.timedelta(days=365))
        status, res = __get__(url.format(
            symbol=scrip, count=count,
            from_dd_mm_yyyy=from_date.strftime('%d-%m-%Y'),
            to_dd_mm_yyyy=to_date.strftime('%d-%m-%Y')))
        if status is False:
            return None
        soup = bs(res, 'lxml')
        raw_data = soup.find('div', {'id': 'csvContentDiv'})
        if raw_data is None:
            print('Unable to find csvContentDiv for {}'.format(scrip))
            print(soup.text)
            return None
        raw_data = raw_data.text
        _data = [[i.replace('"', '').strip() for i in d.split(',')]
                 for d in raw_data.split(':')[:-1]]
        start_pos = 0 if data == [] else 1
        data += _data[start_pos:]
        if from_date <= start:
            break
        else:
            to_date = from_date - datetime.timedelta(days=1)
    df = pd.DataFrame(data[1:], columns=data[0])
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date', inplace=True)
    df.rename({'Symbol': 'symbol',
        'Date': 'date',
        'Open Price': 'open',
        'Close Price': 'close',
        'High Price': 'high',
        'Low Price': 'low',
        'Total Traded Quantity': 'volume'}, axis=1, inplace=True)
    for col in ['open','close','high','low']:
        df[col] = df[col].astype(float)
    df['volume'] = df['volume'].astype(int)
    return df
