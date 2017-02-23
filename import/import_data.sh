#! /usr/bin/bash

# This script exports imports data from csv files to the database
# reads users.csv, facilities.csv, assets.csv, and transfers.csv
if [ "$#" -ne 2 ]; then
    echo "Usage: ./import_dat.sh <dbname> <input dir>"
    exit;
fi

#call python import script, which takes database and directory
python3 inward.py $1 $2
