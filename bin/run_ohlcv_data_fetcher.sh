#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
python ${DIR}/../ohlcv/fetch_ohlcv_data.py $1
