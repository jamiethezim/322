from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
import sys
import datetime
from config import dbname, dbhost, dbport

app = Flask(__name__)
app.secret_key = "Jamie"

conn = psycopg2.connect(dbname=dbname, port=dbport, host=dbhost)
cur = conn.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filter', methods=['GET', 'POST'])
def filter():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
    return render_template('filter.html')

@app.route('/facility', methods=['GET', 'POST'])
def facility():
    if request.method == 'POST':
        fcode = request.form['fcode']
        session['fcode'] = fcode

    SQL = "SELECT asset_tag, fcode FROM assets JOIN asset_at ON asset_pk = asset_fk JOIN facilities ON facility_fk = facility_pk WHERE fcode = '{}'".format(session['fcode'])
    cur.execute(SQL) 
    res = cur.fetchall()
    inv_list = []
    for item in res:
        e = dict()
        e['asset'] = item[0]
        e['facility'] = item[1]
        inv_list.append(e)

    session['inv_list'] = inv_list
    return render_template('facility.html')

@app.route('/transit', methods=['GET', 'POST'])
def transit():
    if request.method == 'POST':
        searchtime = request.form['searchtime']
        timestamp = datetime.datetime.strptime(searchtime, '%Y/%m/%d')
        session['searchtime'] = timestamp

    SQL = "SELECT asset_tag, load_dt, unload_dt FROM assets JOIN asset_on ON asset_pk = asset_fk WHERE load_dt <= '{}' AND '{}' <= unload_dt".format(session['searchtime'], session['searchtime'])
    cur.execute(SQL)
    res = cur.fetchall()
    item_list = []
    for item in res:
        e = dict()
        e['asset'] = item[0]
        e['load_time'] = item[1]
        e['unload_time'] = item[2]
        item_list.append(e)
    session['item_list'] = item_list
    return render_template('transit.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('logout.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
