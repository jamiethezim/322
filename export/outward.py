import csv
import psycopg2
import sys

#usage <dbname>
conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=5432) #the host and port are default and hardcoded here
cur = conn.cursor()

def get_stuff():
	'''
	reports is a list of the filenames we will cycle through - filenames are conveniently named after the corresponding table in the SQL db
	fields is a map from the file name to the column headers that need to be in the csv file
	SQLdict is a map from the file name to the SQL query that will get the information that should go in the file
	
	game plan: cycle through all the files, for each one, query the database, get and write the appropriate headers, zip together the
	column headers and sql data, throw it into the dictionary, and then write it to the file
	'''
	reports = ['users', 'facilities', 'assets', 'transfers']
	fields = {
		'users': ['username', 'password', 'role'],
		'facilities': ['fcode', 'common_name'],
		'assets': ['asset_tag', 'description', 'common_name', 'arrive_dt', 'depart_dt'],
		'transfers': ['asset', 'requestor', 'request_dt', 'approver', 'approval_dt', 'src_fac', 'dest_fac', 'load_dt', 'unload_dt']
	}
	SQLdict = {
		'users': "SELECT username, password, role FROM logins JOIN roles ON role_fk = role_pk",
		'facilities': 'SELECT fcode, common_name from facilities',
		'assets': ('SELECT asset_tag, description, common_name, arrive_dt, depart_dt '
			'FROM assets ' 
			'JOIN asset_at ON asset_pk = asset_fk '
			'JOIN facilities ON facility_fk = facility_pk'),
		'transfers': ('SELECT in_transit.asset, L.username, request_dt, M.username, approval_dt, S.fcode, D.fcode, load_dt, unload_dt '
			'FROM requests '
			'INNER JOIN logins as L on requests.requestor = L.user_pk '
			'INNER JOIN logins as M on requests.approver = M.user_pk '
			'JOIN in_transit on requests.asset = in_transit.asset '
			'INNER JOIN facilities as S on in_transit.src_fac = S.facility_pk '
			'INNER JOIN facilities as D on in_transit.dest_fac = D.facility_pk')
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
