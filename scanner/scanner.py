import os
import pandas as pd

from nseindia import get_historical_price
from chart import Chart


def load_watchlist():
    """ Read all scrips from watchlist file """
    with open('watchlist.txt', 'r') as f:
        watchlist = f.readlines()
    return [w.replace('\n', '') for w in watchlist]


def create_chart(scrip):
    """ Convert historical price info for scrip into chart & bar objects """
    if os.path.exists('tmp/{}.pickle'.format(scrip)):
        data = pd.read_pickle('tmp/{}.pickle'.format(scrip))
    else:
        data = get_historical_price(scrip)
        if data is None:
            print('Unable to fetch data')
            return None
        else:
            pd.to_pickle(data, 'tmp/{}.pickle'.format(scrip))
    return Chart(data)


def check_active_pattern(chart, n=5):
    """ Check if any known candlestick patterns are formed
        in the last *n* days """
    for i, bar in enumerate(reversed(chart.bars[-n:])):
        if bar.pattern != []:
            print('{:10} => t-{:1} ; pattern = {}'.format(chart.name,
                                                     i, bar.pattern))


def scan_watchlist():
    """ Run pattern recognition on all scrips in watchlist """
    for scrip in load_watchlist():
        chart = create_chart(scrip)
        if chart is not None:
            check_active_pattern(chart)
