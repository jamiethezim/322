from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import dbname, dbhost, dbport
#from osnap_crypto import encrypt, decrypt_and_verify
import json
import datetime
import sys
import psycopg2

app = Flask(__name__)
app.secret_key = "Jamie"

conn = psycopg2.connect(dbname=dbname, port=dbport, host=dbhost)
cur = conn.cursor()
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/welcome')
def welcome():
	return render_template('welcome.html',dbname=dbname,dbhost=dbhost,dbport=dbport)

@app.route('/filter', methods=['GET', 'POST'])
def filter():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
    return render_template('filter.html')

@app.route('/rest/list_products', methods=('POST',))
def list_products():
	if request.method=='POST' and 'arguments' in request.form:
		req = json.loads(request.form['arguments'])
	if len(req['compartments']) == 0:
		print('have no compartments')
	
	'''Place holder comment for interacting with database
	as of right now all this function does is parse json and throw it right back into a json reponse 
	'''
	
	#parse the data from the json request, bring in to local sphere
	timestamp = req['timestamp']
	vendor = req['vendor']
	descr = req['description']
	compart = req['compartments'].split(',') #casts to a list
	
	#declare the dictionary to be sent back
	r = dict()
	r['timestamp'] = timestamp
	
	#eventual object in r
	listing = []
	for item in compart:
		e = dict()
		e['vendor'] = vendor
		e['description'] = descr
		e['compartments'] = item
		listing.append(e)

	r['listing'] = listing
   	#package the dictionary into a json object
	res = json.dumps(r) 
	return res
    

@app.route('/rest/add_products', methods=('POST',))
def add_products():
	if request.method=='POST':
		req = json.loads(request.form['arguments'])
	
	timestamp = req['timestamp']
	new_prod = req['new_products']
	lister = []
	for entry in new_prod:
		e = dict()
		e['vendor'] = entry['vendor']
		e['description'] = entry['description']
		e['alt_description'] = entry['alt_description']
		e['compartments'] = entry['compartments']
		lister.append(e)
	# TODO db manipulation using parsed args
	r = dict()
	r['timestamp'] = timestamp
	r['new_products'] = lister
	#ideally here we would package r into a json response
	# in its current manipulation it does nothing but take up space
	respond = dict()
	respond['timestamp'] = timestamp
	respond['result'] = 'OK'
	return json.dumps(respond)

@app.route('/rest/add_asset', methods=('POST',))
def add_asset():
	if request.method=='POST':
		req = json.loads(request.form['arguments'])
	
	timestamp = req['timestamp']
	vendor = req['vendor']
	description = req['description']
	compart = req['compartments']
	fac = req['facility']
	
	#TODO db manipulation
	# find the asset that matches vendor/descrip/facility
	# add to that asset's list of compartments
	respond = dict()
	respond['timestamp'] = timestamp
	respond['result'] = 'OK'
	return json.dumps(respond)




@app.route('/rest/suspend_user', methods=('POST',))
def suspend_user():
    # Check if the call uses crypto
    if request.method=='POST' and 'signature' in request.form and \
            request.form['signature'] != '' and 'arguments' in request.form:
        # do the crypto, expect that hr is on the other side
        (data, skey, nonce) = decrypt_and_verify(request.form['arguments'], request.form['signature'], lost_priv, user_pub)
        
        # Process the request
        req=json.loads(data)
        
        # Prepare the response data
        dat = dict()
        dat['timestamp'] = req['timestamp']
        dat['result'] = 'OK'
        data = json.dumps(dat)
        
        # Encrypt and send the response
        data = encrypt(data,skey,nonce)
        return data
    
    # Try to handle as plaintext
    elif request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data

@app.route('/goodbye')
def goodbye():
    if request.method=='GET' and 'mytext' in request.args:
        return render_template('goodbye.html',data=request.args.get('mytext'))

    # request.form is only populated for POST messages
    if request.method=='POST' and 'mytext' in request.form:
        return render_template('goodbye.html',data=request.form['mytext'])
    return render_template('index.html')


if __name__=="__main__":
    app.run(host='0.0.0.0', port=8080)
