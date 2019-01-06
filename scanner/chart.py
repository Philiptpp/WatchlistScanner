"""Candlestick charting module.

Candlesticks is a charting module to create simple candlestick charts and to
help auto classify candlestick patterns using Bokeh charting library

"""

import datetime

from patterns import find_pattern


class Chart():
    def __init__(self, df, color_up='blue', color_down='red'):
        self.name = df.symbol[0]
        self.color_up, self.color_down = color_up, color_down
        Bar.color_up, Bar.color_down = color_up, color_down
        self.bars = []
        self.__add_data__(df)

    def __add_data__(self, df):
        prev_bar = self.bars[-1] if self.bars else None
        for i, s in df.iterrows():
            new_bar = Bar(s, i, prev_bar)
            self.bars.append(new_bar)
            prev_bar = new_bar
        self.active_bar = self.bars[-1]

    def set_active(self, date):
        if type(date) != datetime.datetime:
            try:
                date = datetime.datetime.strptime(date, '%d%b%Y')
            except:
                raise Exception(
                    'Unknown date format. Must be specified like 01Jan2018.')
        bar = [bar for bar in self.bars if bar.date == date]
        if not bar:
            raise Exception('No data found for date {}'.format(
                date.strftime('%d%b%Y')))
        self.active_bar = bar[0]


class Bar():
    color_up, color_down = 'blue', 'red'

    def __init__(self, series, index, previous):
        self.date = series.date
        self.open = float(series.open)
        self.high = float(series.high)
        self.low = float(series.low)
        self.close = float(series.close)
        self.volume = float(series.volume)
        self.index = index
        self.previous = previous
        self.next = None
        if previous is not None:
            self.previous.next = self
            self.pattern = find_pattern(self)

    def __eq__(self, other):
        return self.date == other.date
