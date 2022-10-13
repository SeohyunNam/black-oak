from datetime import datetime
from distutils.debug import DEBUG
import pandas as pd
import pytz
import random
import string
from typing import List
import logging
import re
import os

def detect_resolution(d1: datetime, d2: datetime) -> int:
    """ Detects the time difference in milliseconds between two datetimes in ms

    :param d1:
    :param d2:
    :return: time difference in milliseconds
    """
    delta = d1 - d2
    return int(delta.total_seconds() * 1e3)


def df_duplicates(df: pd.DataFrame, keep: False) -> int:
    """ returns a data frame with duplicates of the given dataframe

    :param df: data frame
    :param keep: first: Mark duplicates as True except for the first occurrence.
                 last: Mark duplicates as True except for the last occurrence.
                 False: Mark all duplicates as True.
    :return: data frame with duplicates
    """
    return df[df.duplicated(keep=keep)]


def epoch_timestamp_to_ms_timestamp(ts: int) -> int:
    """ Converts an epoch timestamps to a milliseconds timestamp

    :param ts: epoch timestamp in seconds
    :return: timestamp in milliseconds
    """
    return int(ts * 1000)


def ms_timestamp_to_epoch_timestamp(ts: int) -> int:
    """ Converts a milliseconds timestamp to an epoch timestamp

    :param ts: timestamp in miliseconds
    :return: epoch timestamp in seconds
    """
    return int(ts / 1000)


def string_resolution_to_ms(r: str) -> int:
    """ Converts a human readable resolution string to resolution in milliseconds

    :param r: resolution as human readable string
    :return: resolution in milliseconds
    """
    switcher = {
        'minute': 60000,
        'hourly': 3600000,
        'daily': 86400000,
    }

    return int(switcher.get(r))


def string_date_to_ms_timestamp(datetime_string: str, timezone: str = 'UTC') -> int:
    """ converts a datetime string into a timestamp

    :param datetime_string: datetime as string
    :param timezone: timezone
    :return: timestamp in milliseconds
    """
    timezone = pytz.timezone(timezone)
    dt = timezone.localize(datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S'))

    return epoch_timestamp_to_ms_timestamp(dt.timestamp())


def human_readable_resolution(r_ms: int) -> str:
    """ Resolves a resolution in milliseconds to a human readable string

    :param r_ms: resolution in milliseconds
    :return: human readable resolution
    """
    switcher = {
        60000: '1 Minute',
        180000: '3 Minutes',
        300000: '5 Minutes',
        600000: '10 Minutes',
        900000: '15 Minutes',
        1800000: '30 Minutes',
        2700000: '45 Minutes',
        3600000: '1 Hour',
        7200000: '2 Hours',
        10800000: '3 Hours',
        14400000: '4 Hours',
        21600000: '6 Hours',
        43200000: '12 Hour',
        86400000: '1 Day'
    }

    return switcher.get(r_ms, f"Undetectable resolution: {r_ms}")


def ohlcv_columns() -> List[str]:
    """ Returns a list of headers for OHLCV time series

    :return: list of headers for OHLCV time series
    """
    return ['datetime', 'open', 'high', 'low', 'close', 'volume']


def id_generator(length: int = 6, chars: str = string.digits + string.ascii_lowercase + string.ascii_uppercase):
    """ Returns a random id containing chars and digits

    :param length: length of the generated id
    :param chars:  selected range of chars and digits
    :return: a random id containing chars and digits
    """
    return ''.join(random.choice(chars) for _ in range(length))


def percentage(part: int, whole: int) -> float:
    """ Calculates the percentage of a whole and a part

    :param part: part
    :param whole: whole
    :return: percentage of the whole and the part
    """
    return round(100 * float(part) / float(whole), 2)

def extract_units(fetch_log):
    units = set()
    while True:
        line = fetch_log.readline()
        if line.startswith("[INFO] Started to"):
            pass
        else:
            break
        p = re.compile("[A-Z0-9]+/([A-Z0-9]+)")
        patterns =p.search(line)
        unit = patterns.groups()[0]
        units.add(unit)
    return units


def extract_repair_log(target):
    log_data=target.readlines()
    log_list = []
    for i in range(len(log_data)):
        if '\n' == log_data[i]:
            pass
        if 'Loading' in log_data[i]:
            log_list.append(''.join(log_data[i:i+7]))

    log_dict = dict()
    for log in log_list:
        key=log.split('\n')[0].split("/")[1].split("_")[1]
        log_dict[key] = log[:-1]
    return log_dict

def write_toml(symbol, since,until):

    toml_str="""[settings]

    debug = false
    persistence = "file"
    append_file = true
    proxies = [
        ""
    ]
    ratelimit = true

    [exchanges]

        [exchanges.binance]
        filter_symbols = ["{0}"]
        filter_resolutions = ["1h"]
        since = "{1}"
        until = "{2}"
        limit = 365""".format(symbol, since, until)
    path = "toml/"
    file = "{}+{}.toml".format(symbol.replace('/',''),since).replace(' ','_')

    with open(path+file, "w") as f:
        f.write(toml_str)
    return path+file
    
def make_symbol_format(symbolwo,units):
    for unit in units:
        if symbolwo.endswith(unit):
            return "%s/%s"%(symbolwo[:-len(unit)],unit)
    return

# def make_logger(logger,debug,log):

#     formatter = logging.Formatter(fmt='[%(levelname)s] %(message)s')
#     stream_handler = logging.StreamHandler()
#     stream_handler.setLevel(logging.INFO if not debug else logging.DEBUG)
#     stream_handler.setFormatter(formatter)
#     logger.addHandler(stream_handler)

#     if log:
#         file_handler = logging.FileHandler(filename=log)
#         file_handler.setLevel(logging.DEBUG)
#         file_handler.setFormatter(formatter)
#         logger.addHandler(file_handler)