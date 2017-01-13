import psycopg2
import sys
import csv
conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))
cur = conn.cursor()
def products():
    product_file = open('osnap_legacy/product_list.csv', 'r');
    product_file.readline()
    for line in product_file:
        info = line.split(',');
        description = info[2]
        vendor = info[4]
        SQL = "INSERT INTO products (vendor, description) VALUES (%s, %s)"
        data = (vendor, description)
        cur.execute(SQL, data);
        conn.commit();

def facilities():
    fac_list = ("DC", "HQ", "MB005", "NC", "SPNV")
    for fcode in fac_list:
        SQL = 'INSERT INTO facilities (fcode) VALUES (%s)'
        data = (fcode,)
        cur.execute(SQL, data)
        conn.commit()

def inventory(fcode):
    fac_file = "osnap_legacy/{}_inventory.csv".format(fcode)
    with open(fac_file) as inv_file:
        reader = csv.DictReader(inv_file)
        for line in reader:
            SQL = "INSERT INTO assets (asset_tag) VALUES (%s) RETURNING asset_pk"
            data = (line['asset tag'],)
            cur.execute(SQL, data);
            asset_pk = cur.fetchone()[0]

            SQL = "SELECT facility_pk FROM facilities where fcode = '{}'".format(fcode)
            cur.execute(SQL)
            facility_pk = cur.fetchone()[0]

            SQL = "INSERT INTO asset_at (asset_fk, facility_fk) VALUES (%s, %s)"
            data = (asset_pk, facility_pk)
            cur.execute(SQL, data)
            conn.commit()
        

#TODO:
# write remaining functions that parse different csv files.
def main():
    #products()
    facilities()
    
    fac_list = ("DC", "HQ", "MB005", "NC", "SPNV")
    for facility in fac_list:
        inventory(facility)

if __name__ == '__main__':
    main()
##print("INSERT INTO assets (description, asset_tag) VALUES ('item1', 'AT001');')
## -> These are personal notes I took during lecture to help me remember the process of python scripting
# python3 gen_insert.py > insert.sql
# psql lost -f insert.sql # runs the sql script on the database
# does some calculating and parsing of legacy data and prints to stdout the sql statement
#then, pipe this py file to sql script
