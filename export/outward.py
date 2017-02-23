import csv
import psycopg2
import sys

#usage <dbname>
conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=5432) #the host and port are default and hardcoded here
cur = conn.cursor()

def get_users():
	''' this file takes no arguments, writes a file, but does not return the file
	'''
	SQL = "SELECT username, password, role FROM logins JOIN roles ON role_fk = role_pk"
	cur.execute(SQL)
	res = cur.fetchall()
	with open('users.csv', 'w') as users:
		fieldnames = ['username', 'password', 'role', 'active']
		writer = csv.DictWriter(users, fieldnames=fieldnames)
		writer.writeheader()
		for entry in res:
			writer.writerow({'username': entry[0], 'password': entry[1], 'role':entry[2], 'active': True})

def get_facs():
	''' this file takes no arguments, writes a file, but does not return the file
	'''
	SQL = "SELECT fcode, common_name FROM facilities"
	cur.execute(SQL)
	res = cur.fetchall()
	with open('facilities.csv', 'w') as facilities:
		fieldnames = ['fcode', 'common_name']
		writer = csv.DictWriter(facilities, fieldnames=fieldnames)
		writer.writeheader()
		for entry in res:
			writer.writerow({'fcode':entry[0], 'common_name':entry[1]})

def get_assets():
	SQL = "SELECT asset_tag, description, common_name, arrive_dt, depart_dt FROM assets JOIN asset_at ON asset_pk = asset_fk JOIN facilities ON facility_fk = facility_pk"
	cur.execute(SQL)

def get_stuff():
	reports = ['users', 'facilities', 'assets', 'transfers']
	fields = {
		'users': ['username', 'password', 'role'],
		'facilities': ['fcode', 'common_name'],
		'assets': ['asset_tag', 'description', 'common_name', 'arrive_dt', 'depart_dt'],
		'transfers': ['asset', 'username', 'request_dt', 'approver', 'approval_dt', 'src_fac', 'dest_fac', 'load_dt', 'unload_dt']
	}
	SQLdict = {
		'users': "SELECT username, password, role FROM logins JOIN roles ON role_fk = role_pk",
		'facilities': 'SELECT fcode, common_name from facilities',
		'assets': "SELECT asset_tag, description, common_name, arrive_dt, depart_dt FROM assets JOIN asset_at ON asset_pk = asset_fk JOIN facilities ON facility_fk = facility_pk",
		'transfers': "SELECT in_transit.asset, username, request_dt, approver, approval_dt, in_transit.src_fac, in_transit.dest_fac, load_dt, unload_dt FROM requests JOIN in_transit on requests.asset = in_transit.asset JOIN logins on requests.requestor = logins.user_pk"
	}
	
	for filename in reports:
		SQL = SQLdict[filename]
		cur.execute(SQL)
		res = cur.fetchall()
		with open('{}.csv'.format(filename), 'w') as page:
			fieldnames = fields[filename]
			writer = csv.DictWriter(page, fieldnames=fieldnames)
			writer.writeheader()
			for entry in res:
				row = dict(zip(fields[filename], entry))
				writer.writerow(row)


if __name__ == "__main__":
	get_stuff()
