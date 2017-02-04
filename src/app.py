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
		return render_template('login.html')
	elif request.method == 'POST':
		#get login credentials locally
		usn = request.form['username']
		pwd = request.form['password']
		
		#check if user in db
		SQL = "SELECT username, password FROM logins where username = '{}' AND password = '{}'".format(usn, pwd)
		cur.execute(SQL)
		res = cur.fetchall()

		#if user not in db, add credentials, render html saying user added
		if res == []: #no match
			print('no user')
			SQL = "INSERT INTO logins (username, password) VALUES (%s, %s)"
			data = (usn, pwd)
			cur.execute(SQL, data)
			conn.commit()
			print('sql insert successful')
			return render_template('user_added.html')

		#this elif condition is a little goofy... res is a list of tuples,
		#but as long as there are no duplicate usn/pwd combos in db
		#the sql query should only ever find at most 1 result, so it's a list of one tuple
		
		#otherwise user in db and render html saying user exists
		elif usn == res[0][0] and pwd == res[0][1]:
			return render_template('yay.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)
