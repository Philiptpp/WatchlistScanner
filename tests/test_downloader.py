import datetime

import unittest

from scanner.downloader import get_historical_price


sample_set = [
    ("HCLTECH", datetime.datetime(2019, 1, 4), 932.35),
    ("BAJAJ_AUTO", datetime.datetime(2017, 9, 1), 2916.35),
    ("AXISBANK", datetime.datetime(2016, 2, 15), 417.65),
    ("LT", datetime.datetime(2018, 7, 30), 1295.35),
]


class Download_historicals(unittest.TestCase):
    def test_connection(self):
        df = get_historical_price("HCLTECH")
        self.assertIsNotNone(df)

    def test_output_format(self):
        df = get_historical_price("INFY")
        for col in ["symbol", "date", "open", "close", "high", "low", "volume"]:
            self.assertIn(col, df.keys())

    def test_close_price_samples(self):
        for scrip, date, price in sample_set:
            with self.subTest(scrip=scrip, date=date, price=price):
                df = get_historical_price(scrip)
                self.assertIsNotNone(df)
                val = df[df["date"] == date]["close"].values[0]
                self.assertEqual(val, price)

    def test_invalid_symbol(self):
        df = get_historical_price("M&M")  # Invalid symbol, should be MM
        self.assertIsNone(df)
