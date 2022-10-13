#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 18:42:24 2022

@author: seongil-heo
"""

import logging
import sys
import datetime
from dateutil.parser import parse
import re
import click
from lib import util

# fetch_log:"../log/data_entire_fetch.log", target:"../log/data_entire_repair_2.log", (until,last_point) = "2022-07-01 00:00:00")

logging.basicConfig(
    stream=sys.stdout,
    level=20,
    format='[%(levelname)s] %(message)s'
)

@click.command()
@click.argument(
    'fetch_log',
    type=click.File(mode='r'),
)
@click.argument(
    'target',
    type=click.File(mode='r'),
)
@click.option(
    '--until',
    '-u',
    default=datetime.datetime.now().strftime("%Y-%m-%d %H:00:00"),
    help='Last point to collect (default: now)'
)
# @click.option(
#     '--debug',
#     '-d',
#     type=click.BOOL,
#     is_flag=True,
#     default=False,
#     help='Log level (default: False)'
# )
# @click.option(
#     '--log',
#     '-l',
#     default=None,
#     help='save Log (default: False)'
# )


def main(fetch_log,target,until):
    until+=" 00:00:00"
    cnt = 0
    ms_cnt = 0
    ms_symbol = []
    units = util.extract_units(fetch_log)
    logging.debug("%dec units are collected"%len(units))
    
    log_dict = util.extract_repair_log(target)
    
    start_point =  "Date of first data point 2020-07-01 00:00:00"
    missing =  "Found 0 missing data points (0.0% of the data is missing)"

    for k,v in log_dict.items():
        symbol = util.make_symbol_format(k,units)
        if not symbol:
            logging.error("Cannot change symbol name")
            continue
        logging.info("Symbol: %s"%symbol)
        lines = v.split('\n')
        
        if start_point in lines[2]:
            logging.debug("Good Start")
        else:
            logging.debug("Late Start")

        if missing in lines[5]:
            logging.debug("Pass Missing")
        else:
            logging.debug("Missing Data")
            ms_cnt += 1
            ms_symbol.append(symbol)
            continue

        last_str=" ".join(v.split("\n")[3].split()[5:])
        if parse(last_str) < parse(until):
            logging.debug("Lack data")
            file_name = util.write_toml(symbol,last_str,until)
            cnt+=1
            logging.info("Create toml file to re-fetch data %s"%file_name)
        else:
            logging.debug("Full data")
        
        logging.debug("-"*80)

    if ms_symbol:
        with open("mssing_symbol.txt",'w') as f:
            for ms in ms_symbol:
                f.write("%s\n"%ms)

        
    data_ec  = int(lines[-1].split()[0])
    logging.info("Data count: %d & mssing data: %d"%(data_ec,ms_cnt))
    logging.info("%d ec toml fils be created"%cnt)

if __name__ == '__main__':
    main()
