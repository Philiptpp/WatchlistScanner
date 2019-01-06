"""Find Candlestick patterns.

Module to help find candlestick patterns usind candlestick bar info
"""

import os
import configparser

from indicators import *


_config = configparser.ConfigParser()
_config.read(os.path.abspath('config/config.cfg'))


def __value(option):
    return _config.getfloat(section='CANDLESTICK', option=option)


def __body(bar):
    return abs(bar.close - bar.open)


def __upper_shadow(bar):
    return bar.high - max(bar.open, bar.close)


def __lower_shadow(bar):
    return min(bar.open, bar.close) - bar.low


def __percent(percent, bar):
    return bar.close * (__value(percent) / 100)


def __bullish(bar):
    return bar.close > bar.open


def __bearish(bar):
    return bar.open > bar.close


# Single candlestick patterns


def __marubozu(bar):
    # Upper & lower shadow (top & bottom) < IGNORE_TOLERANCE % of price
    # Body between MIN_BODY % to MAX_BODY % of price
    return __upper_shadow(bar) < __percent('IGNORE_TOLERANCE', bar) and \
        __lower_shadow(bar) < __percent('IGNORE_TOLERANCE', bar) and \
        __percent('MIN_BODY', bar) < __body(bar) < __percent('MAX_BODY', bar)


def __bullish_maribozu(bar):
    # Marubozu on bullish candle
    return __marubozu(bar) and __bullish(bar)


def __bearish_maribozu(bar):
    # Marubozu on bearish candle
    return __marubozu(bar) and __bearish(bar)


def __spinning_top(bar):
    # Small real body < MIN_BODY % of price
    # Upper shadow = Lower shadow (< DIFF_TOLLERANCE % difference)
    return (__body(bar) < __percent('MIN_BODY', bar)) and \
        abs(__upper_shadow(bar) - __lower_shadow(bar)) < __percent('DIFF_TOLERANCE', bar) \
        and not __doji(bar)


def __doji(bar):
    # No real body < IGNORE_TOLERANCE % of price
    # Upper shadow = Lower shadow (< DIFF_TOLERANCE % difference)
    return (__body(bar) < __percent('IGNORE_TOLERANCE', bar)) and \
        abs(__upper_shadow(bar) - __lower_shadow(bar)) < __percent('DIFF_TOLERANCE', bar)


def __paper_umbrella(bar):
    # Non-existent upper shadow < IGNORE_TOLERANCE
    # Long lower shadow > LONG_SHADOW
    return __upper_shadow(bar) < __percent('IGNORE_TOLERANCE', bar) and \
        __lower_shadow(bar) > __percent('LONG_SHADOW', bar)


def __hammer(bar):
    # Paper umbrella
    # Downward trend (Low < previous TREND_HISTORY lows)
    return __paper_umbrella(bar) and \
        (bar.low < lowest_low(bar, period=__value('TREND_HISTORY')))


def __hanging_man(bar):
    # Paper umbrella
    # Upward trend (High > previous TREND_HISTORY highs)
    return __paper_umbrella(bar) and \
        (bar.high > highest_high(bar, period=__value('TREND_HISTORY')))


def __shooting_star(bar):
    # Long upper shadow > LONG_SHADOW
    # Non-existent lower shadow < IGNORE_TOLERANCE
    # Upward trend (High > previous TREND_HISTORY highs)
    return __upper_shadow(bar) > __percent('LONG_SHADOW', bar) and \
        __lower_shadow(bar) < __percent('IGNORE_TOLERANCE', bar) and \
        bar.high > highest_high(bar, period=__value('TREND_HISTORY'))


# Multiple candlestick patterns


def __bullish_engulfing(bar):
    # Downward trend (Low < previous TREND_HISTORY lows)
    # Prev bar = Red (bearish) & Cur. bar = Green (bullish)
    # Open < Prev. Close
    # Close > Prev. Open
    return bar.low < lowest_low(bar, period=__value('TREND_HISTORY')) and \
        __bearish(bar.previous) and __bullish(bar) and \
        (bar.open < bar.previous.close) and (bar.close > bar.previous.open)


def __bearish_engulfing(bar):
    # Upward trend (High > previous TREND_HISTORY highs)
    # Prev bar = Green (bullish) & Cur. bar = Red (bearish)
    # Open > Prev. Close
    # Close < Prev. Open
    return bar.high > highest_high(bar, period=__value('TREND_HISTORY')) and \
        __bullish(bar.previous) and __bearish(bar) and \
        (bar.open > bar.previous.close) and (bar.close < bar.previous.open)


def __piercing(bar):
    # Downward trend (Low < previous TREND_HISTORY lows)
    # Prev bar = Red (bearish) & Cur. bar = Green (bullish)
    # Open < Prev. Close
    # Close between 50% to 100% of Prev. candle
    prev_mid = abs(bar.previous.close - bar.previous.open) / 2
    return bar.low < lowest_low(bar, period=__value('TREND_HISTORY')) and \
        __bearish(bar.previous) and __bullish(bar) and \
        bar.open < bar.previous.close and \
        prev_mid < bar.close < bar.previous.open


def __dark_cloud_cover(bar):
    # Upward trend (High > previous TREND_HISTORY highs)
    # Prev bar = Green (bullish) & Cur. bar = Red (bearish)
    # Open > Prev. Close
    # Close between 50% to 100% of Prev. candle
    prev_mid = abs(bar.previous.close - bar.previous.open) / 2
    return bar.high > highest_high(bar, period=__value('TREND_HISTORY')) and \
        __bullish(bar.previous) and __bearish(bar) and \
        bar.open > bar.previous.close and \
        prev_mid > bar.close > bar.previous.open


def __bullish_harami(bar):
    # Downward trend (Low < previous TREND_HISTORY lows)
    # Prev bar = Red (bearish) & Cur. bar = Green (bullish)
    # Open > Prev. Close
    # Close < Prev. Open
    return bar.low < lowest_low(bar, period=__value('TREND_HISTORY')) and \
        __bearish(bar.previous) and __bullish(bar) and \
        bar.open > bar.previous.close and \
        bar.close < bar.previous.open



def __bearish_harami(bar):
    # Upward trend (High > previous TREND_HISTORY highs)
    # Prev bar = Green (bullish) & Cur. bar = Red (bearish)
    # Open < Prev. Close
    # Close > Prev. Open
    return bar.high > highest_high(bar, period=__value('TREND_HISTORY')) and \
        __bullish(bar.previous) and __bearish(bar) and \
        bar.open < bar.previous.close and \
        bar.close > bar.previous.open


def __gap_up_opening(bar):
    # Bullish candle
    # Open > Prev. Close
    return __bullish(bar) and (bar.open > bar.previous.close)


def __gap_down_opening(bar):
    # Bearish candle
    # Open < Prev. Close
    return __bearish(bar) and (bar.open < bar.previous.close)


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
        __bearish_engulfing,
        __piercing,
        __dark_cloud_cover,
        __bullish_harami,
        __bearish_harami,
        __gap_up_opening,
        __gap_down_opening,
        __morning_star,
        __evening_star]

    patterns = [p.__name__.replace('__', '') for p in all_patterns if p(bar)]
    return patterns
