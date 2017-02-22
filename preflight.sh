#! /usr/bin/bash

# This script handles the setup that must occur prior to running web app
# Specifically this script:
#    1. creates the database tables

if [ "$#" -ne 1 ]; then
    echo "Usage: ./preflight.sh <dbname>"
    exit;
fi

# Database prep
# All that this preflight script needs to do is set up the db...
# Andy's script already drops and creates db
cd sql
psql $1 -f create_tables.sql

#cp -R /home/osnapdev/322/src $HOME/wsgi
