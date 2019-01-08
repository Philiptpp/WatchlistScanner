import datetime
import random
import unittest

import pandas as pd

from scanner.chart import Chart
from scanner.indicators import highest_high, lowest_low, sma


df = pd.DataFrame()
data = []


class Indicator_Check(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        global data, df
        for i in range(100):
            data.append(
                [
                    datetime.datetime(2019, 1, 1) + datetime.timedelta(days=1),
                    "TEST",
                    round(random.random() * 1000, 2),
                    round(random.random() * 1000, 2),
                    round(random.random() * 1000, 2),
                    round(random.random() * 1000, 2),
                    round(random.randint(100, 10000)),
                ]
            )
        for i in range(2,6):
            print(max([d[i] for d in data]))
        df = pd.DataFrame(
            data=data,
            columns=["date", "symbol", "open", "high", "low", "close", "volume"],
            index=[d[0] for d in data],
        )

    def test_highest_high(self):
        c = Chart(df)
        self.assertEqual(highest_high(c.bars[-1], period=100), max([d[3] for d in data])        )

    def test_lowest_low(self):
        c = Chart(df)
        self.assertEqual(lowest_low(c.bars[-1], period=100), max([d[4] for d in data]))
