from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import dbname, dbhost, dbport
import json
import datetime
import sys
import psycopg2

app = Flask(__name__)
app.secret_key = 'Jamie'

conn = psycopg2.connect(dbname=dbname, port=dbport, host=dbhost)
cur = conn.cursor()

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
	if request.method == 'GET':
		#loops back to itself
		return render_template('create_user.html') # this has to loop to an html page, otherwise infinite loop!
	elif request.method == 'POST':
		#get login credentials locally
		usn = request.form['username']
		pwd = request.form['password']
		rol = request.form['role']
		#check if user in db
		SQL = "SELECT username, password FROM logins where username = '{}' AND password = '{}'".format(usn, pwd)
		cur.execute(SQL)
		res1 = cur.fetchall()
		#check if role in db
		SQL = "SELECT role_pk from roles where role = '{}'".format(rol)
		cur.execute(SQL)
		res2 = cur.fetchall()

		if not res2: #role type not in db
			SQL = "INSERT INTO roles (role) VALUES (%s) RETURNING role_pk"
			data = (rol,)
			cur.execute(SQL, data)
			role_pk = cur.fetchone()[0]
			conn.commit()
		else:
			role_pk = res2[0]


		#if user/pwd not in db, add them, return html saying they were added
		if not res1: #no match
			SQL = "INSERT INTO logins (username, password, role_fk) VALUES (%s, %s, %s)"
			data = (usn, pwd, role_pk)
			cur.execute(SQL, data)
			conn.commit()
			return render_template('user_added.html')

		#this elif condition is a little goofy... res is a list of tuples,
		#but as long as there are no duplicate usn/pwd combos in db
		#the sql query should only ever find at most 1 result, so it's a list of one tuple
		
		#otherwise user in db and render html saying user exists
		elif usn == res1[0][0] and pwd == res1[0][1]:
			return render_template('yay.html')

@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'GET':	
		return render_template('login.html')
	elif request.method == 'POST':
		usn = request.form['username']		
		pwd = request.form['password']
		
		# I have to do some silly stuff in getting user_pk... this is to make sure
		# that the input password is associated with their username, and that user
		# didn't get lucky typing in some random password that exists in the db
		SQL = "SELECT user_pk, username FROM logins where username = '{}'".format(usn)
		cur.execute(SQL)
		res1 = cur.fetchall()
				
		SQL = "SELECT user_pk, password FROM logins where password = '{}'".format(pwd)
		cur.execute(SQL)
		res2 = cur.fetchall()
		if not res1 or not res2: #if the query didn't find anything
			return render_template('fail.html')
		
		#parse the data from the query result	
		found_usn = res1[0][1]
		found_pwd = res2[0][1]
		pk1 = res1[0][0]
		pk2 = res2[0][0]
		if usn == found_usn and pwd == found_pwd and pk1 == pk2:
			print("found match: {} {} {}".format(found_usn, found_pwd, pk1))
			session['username'] = usn
			session['position'] = user_is(pk1)
			return redirect((url_for('dashboard')))

#helper function -- returns a user's title from their primary key identifier
def user_is(user_pk):
	SQL = "SELECT role FROM logins JOIN roles ON role_fk = role_pk WHERE user_pk = %s"
	data = (user_pk,)
	cur.execute(SQL, data)
	return cur.fetchone()[0]



@app.route('/add_facility', methods=['GET', 'POST'])
def add_facility():
	# need to store the list of facilites as session data
	SQL = "SELECT fcode, common_name FROM facilities"
	cur.execute(SQL)
	res = cur.fetchall()
	keys = ('fcode', 'common_name')
	session['fac_list'] = [dict(zip(keys, row)) for row in res]
	
	if request.method == 'GET':
		return render_template('add_facility.html')
	elif request.method == 'POST':
		fcode = request.form['fcode']
		common_name = request.form['common_name']
		print(request.form)		
		#check if in db
		SQL = "SELECT fcode, common_name from facilities WHERE fcode = '{}' AND common_name = '{}'".format(fcode, common_name)
		cur.execute(SQL)
		res = cur.fetchall()
		if not res: #if not found in db, add it
			SQL = "INSERT INTO facilities (fcode, common_name) VALUES (%s, %s)"
			data = (fcode, common_name)
			cur.execute(SQL, data)
			conn.commit()
			return redirect(url_for('add_facility'))
		elif fcode == res[0][0] and common_name == res[0][1]:
			return render_template('fac_duplicate.html')


		
@app.route('/dashboard', methods=['GET'])
def dashboard():
	return render_template('dashboard.html')


@app.route('/add_asset', methods=['GET', 'POST'])
def add_asset():
	SQL = "SELECT asset_tag, description FROM assets"
	cur.execute(SQL)
	res = cur.fetchall()
	keys = ('asset_tag', 'description')
	session['asset_list'] = [dict(zip(keys, row)) for row in res]

	SQL = "SELECT common_name from facilities"
	cur.execute(SQL)
	res = cur.fetchall()
	session['fac_options'] = [row[0] for row in res]
	print(session['fac_options'])
	if request.method == 'GET':
		return render_template('add_asset.html')
	elif request.method == 'POST':
		tag = request.form['asset_tag']
		loc = request.form['common_name']
		descr = request.form['description']
		time = request.form['date']
		print(tag, loc, descr, time)

		#check if asset tag in db
		SQL = "SELECT asset_tag from assets WHERE asset_tag = '{}'".format(tag)
		cur.execute(SQL)
		res = cur.fetchall()
		if not res: #if asset not in db, add it
			SQL = "INSERT INTO assets (asset_tag, description) VALUES (%s, %s) RETURNING asset_pk"
			data = (tag, descr)
			cur.execute(SQL, data)
			asset_pk = cur.fetchone()[0]
			conn.commit()
			
			#find the facility key where the asset should go
			SQL = "SELECT facility_pk from facilities WHERE common_name = '{}'".format(loc)
			cur.execute(SQL)
			facility_pk = cur.fetchone()[0]
			print(facility_pk)

			#link asset to its location in asset_at table
			SQL = "INSERT INTO asset_at VALUES (%s, %s, %s)"
			data = (asset_pk, facility_pk, time)
			cur.execute(SQL, data)
			conn.commit()
			return redirect(url_for('add_asset'))
		elif tag == res[0][0]:
			return render_template('asset_dup.html')

@app.route('/dispose_asset', methods=['GET', 'POST'])
def dispose_asset():
	user = session['username']
	SQL = "SELECT role from logins JOIN roles ON logins.role_fk = roles.role_pk WHERE username = '{}'".format(user)
	cur.execute(SQL)
	title = cur.fetchone()[0]
	if title != 'logistics officer':
		return render_template('no_office.html')
	if request.method == 'GET':
		return render_template('dispose_asset.html')
	if request.method == 'POST':
		tag = request.form['asset_tag']
		time = request.form['date'] #this is a string
		#check if asset in db
		SQL = "SELECT asset_tag, disposed from assets WHERE asset_tag LIKE '{}'".format(tag)
		cur.execute(SQL)
		res = cur.fetchall() #tuple of strings and datetime object
		if not res:
			return render_template('no_asset.html')
		elif not res[0][1] is None: #if disposed
			return render_template('dispose.html')
		else: #update disposed status
			SQL = "UPDATE assets SET disposed = %s where asset_tag = %s"
			data = (time, tag)
			cur.execute(SQL, data)
			conn.commit()
			return render_template('dashboard.html')


@app.route('/asset_report', methods=['GET', 'POST'])
def asset_report():
	if request.method == 'GET':
		return render_template('asset_report.html')
	elif request.method == 'POST':
		loc = request.form['common_name']
		time = request.form['date']
		if not time: #if no time is specified in text field, code breaks
			return redirect(url_for('asset_report'))		
		SQL = "SELECT asset_tag, description, common_name, arrive_dt FROM assets JOIN asset_at ON assets.asset_pk = asset_at.asset_fk JOIN facilities ON asset_at.facility_fk = facilities.facility_pk WHERE arrive_dt = '{}'".format(time)
		if loc != '': #if a location was specified
			SQL += " AND common_name = '{}'".format(loc)
		cur.execute(SQL)
		res = cur.fetchall()
		keys = ('asset_tag', 'description', 'common_name', 'arrive_dt')
		session['report'] = [dict(zip(keys, row)) for row in res]
		return redirect(url_for('asset_report'))


@app.route('/transfer_req', methods=['GET', 'POST'])
def transfer_req():
	if session['position'] != 'logistics officer':
		return render_template('not_officer.html')
	if request.method == 'GET':
		return render_template('transfer_req.html')
	elif request.method == 'POST':
		asset = request.form['asset_tag']
		src = request.form['src_common_name']
		dest = request.form['dest_common_name']
		#flask request object does not have a date time attribute
		#so I just have to get the clock time when the request comes in
		time = datetime.datetime.now()
		
		#I am aware that I reassign requestor from username to user primary key identifier
		requestor = session['username']
		SQL = "SELECT user_pk from logins WHERE username = '{}'".format(requestor)
		cur.execute(SQL)
		requestor = cur.fetchone()[0]

		#check if the asset tag, src fac, and dest fac are all in DB
		SQL = "SELECT asset_pk from assets WHERE asset_tag = '{}'".format(asset)
		cur.execute(SQL)
		asset_res = cur.fetchone()[0]
		
		SQL = "SELECT facility_pk from facilities WHERE common_name = '{}'".format(src)
		cur.execute(SQL)
		src_res = cur.fetchone()[0]
		
		SQL = "SELECT facility_pk from facilities WHERE common_name = '{}'".format(dest)
		cur.execute(SQL)
		dest_res = cur.fetchone()[0]
	
		#validity checks
		if not asset_res:
			return '<!DOCTYPE HTML> asset does not exist'
		if not src_res:
			return '<!DOCTYPE HTML> source facility does not exist'
		if not dest_res:
			return '<!DOCTYPE HTML> destination facility does not exist'
		
		#process and insert the request
		SQL = "INSERT INTO requests (requestor, request_dt, src_fac, dest_fac, asset) VALUES (%s, %s, %s, %s, %s)"
		data = (requestor, time, src_res, dest_res, asset_res)
		cur.execute(SQL, data)
		conn.commit()
		return '<!DOCTYPE HTML> transfer request successfully submitted'


#Extra credit - skeleton implemented only to avoid bugs
@app.route('/transfer_report', methods=['GET', 'POST'])
def transfer_report():
	return render_template('transfer_report.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)
