
def products():
    product_file = open('osnap_legacy/product_list.csv', 'r');
    i = 0
    for line in product_file:
        info = line.split(',');
        name = info[0]
        model = info[1]
        description = info[2]
        unit_price = info[3]
        vendor = info[4]
        compartments = info[5]
        i = i + 1
        print("INSERT INTO products (product_pk, vendor, description) VALUES ('{}', '{}', '{}');".format(i, vendor, description))

#TODO:
# write remaining functions that parse different csv files.

def main():
    products()

if __name__ == '__main__':
    main()
##print("INSERT INTO assets (description, asset_tag) VALUES ('item1', 'AT001');')
## -> These are personal notes I took during lecture to help me remember the process of python scripting
# python3 gen_insert.py > insert.sql
# psql lost -f insert.sql # runs the sql script on the database
# does some calculating and parsing of legacy data and prints to stdout the sql statement
#then, pipe this py file to sql script
