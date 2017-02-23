#! /usr/bin/bash

# This script exports data currently in the database to csv files
# will create, users.csv, facilities.csv, assets.csv, and transfers.csv
if [ "$#" -ne 1 ]; then
    echo "Usage: ./export_data.sh <dbname> <output dir>"
    exit;
fi
#$1 is dbname
#$2 is the path for the directory where the files will be read from


#call python export script
python3 outward.py
