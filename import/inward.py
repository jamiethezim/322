import csv
import psycopg2
import sys

conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=5432) #the host and port are default and hardcoded here
cur = conn.cursor()
input_dir = sys.argv[2]

def import_users(user_file):
	with open(user_file) as user_file:
		reader = csv.DictReader(user_file)
		for line in reader:
			#check if role is in roles table
			SQL = "select role_pk from roles where role = '{}'".format(line['role'])
			cur.execute(SQL)
			res = cur.fetchall()
			if not res: #if the role is not the table, insert it
				SQL = "INSERT INTO roles (role) VALUES (%s) RETURNING role_pk"
				data = (line['role'],)
				cur.execute(SQL, data)
				res = cur.fetchone()[0]
			else:
				res = res[0]
			#either way, we got the role_fk that is attached to the user
			
			SQL = "INSERT INTO logins (username, password, role_fk) VALUES (%s, %s, %s)"
			data = (line['username'], line['password'], res)
			cur.execute(SQL, data)
			conn.commit() #we have to commit everytime because entries into the roles table each iteration might change



def import_facs(fac_file):
	''' input() -> string repr. of file name, i.e.: 'facilities.csv'
	'''
	with open(fac_file) as fac_file:
		reader = csv.DictReader(fac_file)
		for line in reader:
			SQL = "INSERT INTO facilities (fcode, common_name) VALUES (%s, %s)"
			data = (line['fcode'], line['common_name'])
			cur.execute(SQL, data)
		conn.commit()	


def import_assets(assets_file):
	with open(assets_file) as assets_file:
		reader = csv.DictReader(assets_file)
		for line in reader:
			SQL = "INSERT INTO assets (asset_tag, description) VALUES (%s, %s) RETURNING asset_pk"
			data = (line['asset_tag'], line['description'])
			cur.execute(SQL, data)
			asset_pk = cur.fetchone()[0]

			#get the facility_fk from the common name
			SQL = "Select facility_pk from facilities where common_name = %s"
			data = (line['common_name'],)
			cur.execute(SQL, data)
			facility_pk = cur.fetchone()[0]

			#insert into asset_at table
			SQL = "INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt, depart_dt) VALUES (%s, %s, %s, %s)"
			dep = line['depart_dt'] if line['depart_dt'] != "" else None #ternary - timestamp is null if the string from csv is empty string
			data = (asset_pk, facility_pk, line['arrive_dt'], dep)
			cur.execute(SQL, data)
			
			conn.commit()
			
def import_transfers(transfer_file):
	with open(transfer_file) as transfer_file:
		reader = csv.DictReader(transfer_file)
		for line in reader:
			#needs to get primary key identifiers for requestor and approver (currently their username)
			SQL = "SELECT user_pk from logins where username = '{}'".format(line['requestor'])
			cur.execute(SQL)
			reqr = cur.fetchone()[0]
			SQL = "SELECT user_pk from logins where username = '{}'".format(line['approver'])
			cur.execute(SQL)
			appr = cur.fetchone()[0]
			
			#need to get facility fk identifier for src_fac and dest_fact (currently in csv as fcode identifier)
			SQL = "Select facility_pk from facilities where fcode = '{}'".format(line['src_fac'])
			cur.execute(SQL)
			src = cur.fetchone()[0]
			SQL = "Select facility_pk from facilities where fcode = '{}'".format(line['dest_fac'])
			cur.execute(SQL)
			dest = cur.fetchone()[0]
			
			#import data into requests table
			SQL = "INSERT INTO requests (requestor, request_dt, src_fac, dest_fac, asset, approver, approval_dt) VALUES (%s, %s, %s, %s, %s, %s, %s)"
			data = (reqr, line['request_dt'], src, dest, line['asset'], appr, line['approval_dt'])
			cur.execute(SQL, data)

			#import data into in_transit table
			SQL = "INSERT INTO in_transit (asset, src_fac, dest_fac, load_dt, unload_dt) VALUES (%s, %s, %s, %s, %s)"
			data = (line['asset'], src, dest, line['load_dt'], line['unload_dt'])
			cur.execute(SQL, data)
		conn.commit()




if __name__ == "__main__":
	import_users('{}/users.csv'.format(input_dir))
	import_facs('{}/facilities.csv'.format(input_dir))
	#import_facs must be called BEFORE imports assets.csv or transfers.csv
	# because they both refer to facilities table
	import_assets('{}/assets.csv'.format(input_dir))
	import_transfers('{}/transfers.csv'.format(input_dir))
