import os
import datetime
import time
import pandas as pd

from nseindia import get_historical_price
from chart import Chart


class Scanner:
    def __init__(self, watchlist_file=None):
        self.__ignore_list = []
        if watchlist_file is None:
            __watchlist = []
        else:
            self.load_watchlist(watchlist_file)
 
    def load_watchlist(self, watchlist_file):
        """ Read all scrips from watchlist file """
        with open(watchlist_file, 'r') as f:
            watchlist = f.readlines()
        self.__watchlist = [w.replace('\n', '') for w in watchlist]
        print('Loaded {} symbols from watchlist.'.format(len(self.__watchlist)))

    @staticmethod
    def _create_chart(scrip):
        """ Convert historical price info for scrip into chart & bar objects """
        loaded=False
        if os.path.exists('tmp/{}.pickle'.format(scrip)):
            ctime = os.path.getctime('tmp/{}.pickle'.format(scrip))
            if datetime.datetime.strptime(time.ctime(ctime), "%a %b %d %H:%M:%S %Y").date() < datetime.datetime.today().date():
                os.remove('tmp/{}.pickle'.format(scrip))
            else:
                data = pd.read_pickle('tmp/{}.pickle'.format(scrip))
                loaded = True
        if not loaded:
            data = get_historical_price(scrip)
            if data is None:
                print('Unable to fetch data')
                return None
            else:
                pd.to_pickle(data, 'tmp/{}.pickle'.format(scrip))
        return Chart(data)

    def __check_active_pattern(self, chart, n=5):
        """ Check if any known candlestick patterns are formed
            in the last *n* days """
        for i, bar in enumerate(reversed(chart.bars[-n:])):
            if bar.pattern != []:
                _ = [print('{:10} => t-{:1} ; pattern = {}'.format(
                        chart.name, i, pattern)) for pattern in bar.pattern \
                        if pattern not in self.__ignore_list]
    
    def scan_watchlist(self):
        """ Run pattern recognition on all scrips in watchlist """
        for scrip in self.__watchlist:
            chart = Scanner._create_chart(scrip)
            if chart is not None:
                self.__check_active_pattern(chart)

    @property
    def ignore_list(self):
        return self.__ignore_list
    
    @ignore_list.setter
    def ignore_list(self, ignore_patterns):
        self.__ignore_list = ignore_patterns
