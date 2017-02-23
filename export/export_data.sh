#! /usr/bin/bash

# This script exports data currently in the database to csv files
# will create, users.csv, facilities.csv, assets.csv, and transfers.csv
if [ "$#" -ne 2 ]; then
    echo "Usage: ./export_data.sh <dbname> <output dir>"
    exit;
fi

#regardless of the outputdir existing, it needs to be an empty directory before we populate it
rm -rf $2
mkdir $2

#call python export script
python3 outward.py $1

#move all the csv files to the location
mv *.csv $2
