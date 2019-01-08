from datetime import datetime
import unittest

import pandas as pd

from scanner.chart import Chart
import scanner.patterns as p

# __morning_star
# __evening_star

data = [
    # One candle patterns
    ["bullish_maribozu", datetime(2019, 1, 1), "TEST", 1000, 1050, 1000, 1050, 100],
    ["bearish_maribozu", datetime(2019, 1, 1), "TEST", 1050, 1050, 1000, 1000, 100],
    ["spinning_top", datetime(2019, 1, 1), "TEST", 1000, 1200, 800, 1008, 100],
    ["doji", datetime(2019, 1, 1), "TEST", 1000, 1200, 800, 1000, 100],
    ["hammer", datetime(2019, 1, 1), "TEST", 2000, 2100, 1800, 1900, 100],
    ["hammer", datetime(2019, 1, 2), "TEST", 1100, 1100, 500, 1000, 100],
    ["hanging_man", datetime(2019, 1, 1), "TEST", 500, 800, 300, 600, 100],
    ["hanging_man", datetime(2019, 1, 2), "TEST", 1000, 1100, 500, 1100, 100],
    ["shooting_star", datetime(2019, 1, 1), "TEST", 500, 800, 300, 600, 100],
    ["shooting_star", datetime(2019, 1, 2), "TEST", 1000, 1300, 900, 900, 100],
    # Two candle patterns
    ["bullish_engulfing", datetime(2019, 1, 1), "TEST", 1000, 1000, 900, 900, 100],
    ["bullish_engulfing", datetime(2019, 1, 2), "TEST", 800, 1100, 800, 1100, 100],
    ["bearish_engulfing", datetime(2019, 1, 1), "TEST", 900, 1000, 900, 1000, 100],
    ["bearish_engulfing", datetime(2019, 1, 2), "TEST", 1100, 1100, 800, 800, 100],
    ["piercing", datetime(2019, 1, 1), "TEST", 1000, 1000, 900, 900, 100],
    ["piercing", datetime(2019, 1, 2), "TEST", 800, 975, 800, 975, 100],
    ["dark_cloud_cover", datetime(2019, 1, 1), "TEST", 900, 1000, 900, 1000, 100],
    ["dark_cloud_cover", datetime(2019, 1, 2), "TEST", 1100, 1100, 925, 925, 100],
    ["bullish_harami", datetime(2019, 1, 1), "TEST", 1000, 1000, 900, 900, 100],
    ["bullish_harami", datetime(2019, 1, 2), "TEST", 925, 975, 925, 975, 100],
    ["bearish_harami", datetime(2019, 1, 1), "TEST", 900, 1000, 900, 1000, 100],
    ["bearish_harami", datetime(2019, 1, 2), "TEST", 975, 975, 925, 925, 100],
    ["gap_up_opening", datetime(2019, 1, 1), "TEST", 900,  1100, 800, 1000, 100],
    ["gap_up_opening", datetime(2019, 1, 2), "TEST", 1200, 1400, 1200, 1300, 100],
    ["gap_down_opening", datetime(2019, 1, 1), "TEST", 1000,  1100, 800, 900, 100],
    ["gap_down_opening", datetime(2019, 1, 2), "TEST", 700, 700, 500, 600, 100],
]
df = pd.DataFrame(
    data=data,
    columns=["pattern", "date", "symbol", "open", "high", "low", "close", "volume"],
    index=[d[1] for d in data]
)


class Candlestick_patterns(unittest.TestCase):
    def test_pattern(self):
        for pattern in set([d[0] for d in data]):
            with self.subTest(pattern=pattern):
                c = Chart(df[df.pattern == pattern])
                self.assertIn(pattern, p.find_pattern(c.bars[-1]))
