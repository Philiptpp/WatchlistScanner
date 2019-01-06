"""Technical Indicators.

Commonly used technical indicators
"""


def lowest_low(bar, period=100):
    if bar is None:
        return 0
    lowest_low = bar.high
    for _ in range(int(period)):
        prev_bar = bar.previous
        if prev_bar is None:
            break
        else:
            lowest_low = min(lowest_low, bar.low)
    return lowest_low


def highest_high(bar, period=100):
    if bar is None:
        return 0
    highest_high = bar.low
    for _ in range(int(period)):
        prev_bar = bar.previous
        if prev_bar is None:
            break
        else:
            highest_high = max(highest_high, bar.high)
    return highest_high


def sma(bar, period=15):
    rolling_sum = 0
    for _ in range(period):
        if bar is not None and bar.previous is not None:
            bar = bar.previous
            rolling_sum += bar.close
        else:
            return 0
    return (rolling_sum / period)
