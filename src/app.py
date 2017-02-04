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
		return render_template('yay.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)
