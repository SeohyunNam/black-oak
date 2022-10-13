#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
LOG_DIR=$(echo ${DIR}"/../log/")
TOML_DIR=$(echo ${DIR}"/../toml/")

log_file_fetch=$(echo $1 | cut -d '_' -f1 -f2)
log_file_repair=$log_file_fetch"_repair_2.log"
echo ${LOG_DIR}$1 ${LOG_DIR}${log_file_repair} $2
python ${DIR}/../ohlcv/create_toml.py ${LOG_DIR}$1 ${LOG_DIR}${log_file_repair} -u $2

for toml in `ls ${DIR}/../toml/`; do
    python ${DIR}/../ohlcv/fetch_ohlcv_data.py ${TOML_DIR}${toml} | tee ${DIR}/../log/after/${toml}.log
done


