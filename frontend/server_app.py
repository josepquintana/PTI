#############################################################################################################################################################
#############################################################################################################################################################

import json
import hashlib
import requests
from flask import Flask, jsonify, request, redirect, make_response, abort, url_for, render_template, send_from_directory
from flask_cors import CORS
 
# Flask configuration
app = Flask(__name__, template_folder='www/', static_url_path='', static_folder='www/')
app.config["DEBUG"] = True
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
# app.config['SERVER_NAME'] = website_url 

#############################################################################################################################################################
""" MAIN APP WEBSITE """
#############################################################################################################################################################

@app.route('/', methods=['GET'])
def root():
    if is_cookie_valid():
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/home', methods=['GET'])
def home():
    if is_cookie_valid():
        return render_template("home.html")
    else:
        return redirect(url_for('login'))
   
@app.route('/signup', methods=['GET'])
def signup():
    if is_cookie_valid():
        return redirect(url_for('home'))
    else:
        return render_template("signup.html")
   
@app.route('/login', methods=['GET'])
def login():
    if is_cookie_valid():
        return redirect(url_for('home'))
    else:
        return render_template("login.html")
   
#############################################################################################################################################################
""" PROCESS CLIENT REQUESTS """
#############################################################################################################################################################
  
@app.route('/run/view_open_bids', methods=['GET'])
def run_view_open_bids():  
    res = requests.get('http://10.4.41.142/api/v1/bids/list')
    return res.text, res.status_code


@app.route('/run/list_bid_by_id/<bid_id>', methods=['GET'])
def run_list_bid_by_id(bid_id):  
    res = requests.get('http://10.4.41.142/api/v1/bids/list/id/' + bid_id)
    return res.text, res.status_code
    
  
@app.route('/run/create_new_bid', methods=['POST'])
def run_create_new_bid():
    buy_amount = request.form.get("buy_amount", type = str)
    buy_currency = request.form.get("buy_currency", type = str)
    sell_amount = request.form.get("sell_amount", type = str)
    sell_currency = request.form.get("sell_currency", type = str)
    API_KEY = request.form.get("API_KEY", type = str)
    
    pload = { 'buy_amount': buy_amount, 'buy_currency': buy_currency, 'sell_amount': sell_amount, 'sell_currency': sell_currency, 'API_KEY': API_KEY }
    res = requests.post('http://10.4.41.142/api/v1/bids/new', data = pload)
    return res.text, res.status_code
  
  
@app.route('/run/block_bid/<bid_id>', methods=['GET'])
def run_block_bid(bid_id):  
    res = requests.get('http://10.4.41.142/api/v1/bids/block/' + bid_id)
    return res.text, res.status_code
    
    
@app.route('/run/unblock_and_delete_bid/<bid_id>', methods=['GET'])
def run_unblock_and_delete_bid(bid_id):  
    res = requests.get('http://10.4.41.142/api/v1/bids/unblock/' + bid_id)
    return res.text, res.status_code
    
"""
@app.route('/run/delete_bid/<bid_id>', methods=['POST'])
def run_delete_bid(bid_id):  
    API_KEY = request.form.get("API_KEY", type = str)
    pload = { 'API_KEY': API_KEY }
    res = requests.post('http://10.4.41.142/api/v1/bids/delete/' + bid_id, data = pload)
    return res.text, res.status_code
"""  
 
  
@app.route('/run/signup', methods=['POST'])
def run_signup():  
    if request.form.get("signup-form-submitted", type = str) is None:
        abort(400)
        
    name = request.form.get("name", type = str)
    email = request.form.get("email", type = str)
    password = request.form.get("password", type = str)
    repeat_password = request.form.get("repeat_password", type = str)
      
    if name is None or email is None or password is None or repeat_password is None:
        abort(400)
        
    pload = { "name": name, "email": email, "password": password, "repeat_password": repeat_password }
    res = requests.post('http://10.4.41.142/api/v1/users/signup', data = pload)
    return res.text, res.status_code
    

@app.route('/run/login', methods=['POST'])
def run_login():  
    if request.form.get("login-form-submitted", type = str) is None:
        abort(400)
        
    email = request.form.get("email", type = str)
    password = request.form.get("password", type = str)
    
    if email is None or password is None:
        abort(400)
        
    pload = { "email": email, "password": password }
    res_post = requests.post('http://10.4.41.142/api/v1/users/login', data = pload)
    
    # Set Log In cookie
    if res_post.status_code == 200 and json.loads(res_post.text)['user'] == "authenticated":
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        response = make_response(res_post.text)
        response.set_cookie("itoken_user_email", email, max_age=60*60*24)
        response.set_cookie("itoken_user_key", hashed_password, max_age=60*60*24)
        return response, 200
    
    else:
        return res_post.text, res_post.status_code
   
   
@app.route('/run/logout', methods=['POST'])
def run_logout():  
    if request.form.get("logout-form-submitted", type = str) is None:
        abort(400)
    
    # Destroy Log In cookie
    response = make_response()
    response.delete_cookie("itoken_user_email")
    response.delete_cookie("itoken_user_key")
        
    # Redirect to login page
    return redirect(url_for('login'))
   
    
#############################################################################################################################################################
""" CHECK LOG IN COOKIE VALIDITY """
#############################################################################################################################################################
    
def is_cookie_valid():
    itoken_user_email = request.cookies.get("itoken_user_email")
    itoken_user_key = request.cookies.get("itoken_user_key")
    
    if itoken_user_email is None or itoken_user_key is None:
        return False
    
    pload = { "itoken_user_email": itoken_user_email, "itoken_user_key": itoken_user_key }
    res_post = requests.post('http://10.4.41.142/api/v1/users/login/cookie', data = pload)
    
    if res_post.status_code == 200 and json.loads(res_post.text)['user'] == "valid cookie":
        return True
    else:
        return False
    
#############################################################################################################################################################
""" SERVER STATIC ABI FILES """
#############################################################################################################################################################
    
@app.route('/files/abis/BarnaToken.json', methods=['GET'])
def files_BarnaToken():
    return send_from_directory("abis", "BarnaToken.json")
    
@app.route('/files/abis/FiberToken.json', methods=['GET'])
def files_FiberToken():
    return send_from_directory("abis", "FiberToken.json")

@app.route('/files/abis/UpcToken.json', methods=['GET'])
def files_UpcToken():
    return send_from_directory("abis", "UpcToken.json")
    
@app.route('/files/abis/CatToken.json', methods=['GET'])
def files_CatToken():
    return send_from_directory("abis", "CatToken.json")
    
#############################################################################################################################################################
""" TEST ROUTE """
#############################################################################################################################################################

@app.route('/test', methods=['GET'])
def test():
    response = {
        "test": "success"
    }
	
    return jsonify(response), 200

#############################################################################################################################################################
""" ERROR HANDLERS """
#############################################################################################################################################################

@app.errorhandler(400)
def error_handler_400(error):
	response = { "error": { "code": 400, "message": "Bad Request" } }
	return jsonify(response), 400

@app.errorhandler(401)
def error_handler_401(error):
	response = { "error": { "code": 401, "message": "Unauthorized" } }
	return jsonify(response), 401

@app.errorhandler(403)
def error_handler_403(error):
	response = { "error": { "code": 403, "message": "Forbidden" } }
	return jsonify(response), 403

@app.errorhandler(404)
def error_handler_404(error):
    response = { "error": { "code": 404, "message": "Not Found" } }
    return jsonify(response), 404
	
#############################################################################################################################################################
""" MAIN ENTRY POINT """
#############################################################################################################################################################

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=80, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
	
    app.run(host='0.0.0.0', port=port)	
	
    
    