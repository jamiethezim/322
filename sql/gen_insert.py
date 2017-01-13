import psycopg2

#cur.execute(""sql command)
def products():
    product_file = open('osnap_legacy/product_list.csv', 'r');
    for line in product_file:
        info = line.split(',');
        name = info[0]
        model = info[1]
        description = info[2]
        unit_price = info[3]
        vendor = info[4]
        compartments = info[5]
        print("INSERT INTO products (vendor, description) VALUES ('{}', '{}');".format(vendor, description))

        
def main():
    #conn = psycopg2.connect("dbname=homework2 user=postgres")
    #cur = con.cursor()
    products()

if __name__ == '__main__':
    main()
##print("INSERT INTO assets (description, asset_tag) VALUES ('item1', 'AT001');')
# python3 gen_insert.py > insert.sql
# psql lost -f insert.sql # runs the sql script on the database
# does some calculating and parsing of legacy data and prints to stdout the sql statement
#then, pipe this py file to sql script
