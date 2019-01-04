import datetime

import pytest

from scanner.nseindia import get_historical_price


def connection_test():
    df = get_historical_price('HCLTECH',
                            datetime.datetime(2019, 1, 4),
                            datetime.datetime(2019, 1, 4))
    print(df['close'])
    assert (df['close'].values[0] == 932.35)
