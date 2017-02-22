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
			return redirect((url_for('dashboard')))

@app.route('/add_facility', methods=['GET', 'POST'])
def add_facility():
	if request.method == 'GET':
		return render_template('add_facility.html')
	elif request.method == 'POST':
		return			


		
@app.route('/dashboard', methods=['GET'])
def dashboard():
	return render_template('dashboard.html')



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)
