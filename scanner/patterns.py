"""Find Candlestick patterns.

Module to help find candlestick patterns usind candlestick bar info
"""

from indicators import *


def __body(bar):
    return abs(bar.close - bar.open)


def __upper_shadow(bar):
    return bar.high - max(bar.open, bar.close)


def __lower_shadow(bar):
    return min(bar.open, bar.close) - bar.low


def __percent(bar, percent):
    return bar.close * (percent / 100)


def __bullish(bar):
    return bar.close > bar.open


def __bearish(bar):
    return bar.open > bar.close


# Single candlestick patterns


def __marubozu(bar):
    # Upper & lower shadow (top & bottom) < 0.25% of price
    # Body between 1% to <10% of price
    return __upper_shadow(bar) < __percent(bar, 0.25) and \
        __lower_shadow(bar) < __percent(bar, 0.25) and \
        __percent(bar, 1) < __body(bar) < __percent(bar, 10)


def __bullish_maribozu(bar):
    # Marubozu on bullish candle
    return __marubozu(bar) and __bullish(bar)


def __bearish_maribozu(bar):
    # Marubozu on bearish candle
    return __marubozu(bar) and __bearish(bar)


def __spinning_top(bar):
    # Small real body <1% of price
    # Upper shadow = Lower shadow (<0.25% difference)
    return (__body(bar) < __percent(bar, 1)) and \
        abs(__upper_shadow(bar) - __lower_shadow(bar)) < __percent(bar, 0.1) \
        and not __doji(bar)


def __doji(bar):
    # No real body <0.5% of price
    # Upper shadow = Lower shadow (<0.25% difference)
    return (__body(bar) < __percent(bar, 0.5)) and \
        abs(__upper_shadow(bar) - __lower_shadow(bar)) < __percent(bar, 0.1)


def __paper_umbrella(bar):
    # Non-existent upper shadow < (body / 4)
    # Long lower shadow > 2 * body
    return __upper_shadow(bar) < (__body(bar) / 4) and \
        __lower_shadow(bar) > (2 * __body(bar))


def __hammer(bar):
    # Paper umbrella
    # Downward trend
    # Low < previous 5 bar lows
    return __paper_umbrella(bar) and \
        (sma(bar, 5) < sma(bar.previous, 5)) and \
        (bar.low < lowest_low(bar))


def __hanging_man(bar):
    # Paper umbrella
    # Upward trend
    # High > previous 5 bar highs
    return __paper_umbrella(bar) and \
        (sma(bar, 5) > sma(bar.previous, 5)) and \
        (bar.high > highest_high(bar))


def __shooting_star(bar):
    # Upper shadow > 2 * body
    # Non-existent lower shadow < (body / 4)
    # Upward trend
    # High > previous 5 bar highs
    return __upper_shadow(bar) > (2 * __body(bar)) and \
        (__lower_shadow(bar) < (__body(bar) / 4)) and \
        (sma(bar, 5) > sma(bar.previous, 5)) and \
        (bar.high > highest_high(bar))


# Multiple candlestick patterns


def __bullish_engulfing(bar):
    pass


def __piercing(bar):
    pass


def __dark_cloud_cover(bar):
    pass


def __bullish_harami(bar):
    pass


def __bearish_harami(bar):
    pass


def __gaps(bar):
    pass


def __morning_star(bar):
    pass


def __evening_star(bar):
    pass


def find_pattern(bar):
    all_patterns = [
        __bullish_maribozu,
        __bearish_maribozu,
        __spinning_top,
        __doji,
        __hammer,
        __hanging_man,
        __shooting_star,
        __bullish_engulfing,
        __piercing,
        __dark_cloud_cover,
        __bullish_harami,
        __bearish_harami,
        __gaps,
        __morning_star,
        __evening_star]

    patterns = [p.__name__.replace('__', '') for p in all_patterns if p(bar)]
    return patterns
