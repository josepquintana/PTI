#############################################################################################################################################################
#############################################################################################################################################################

import json
import requests
from flask import Flask, jsonify, request, abort, render_template, send_from_directory
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
def home():
    return render_template("index.html")
    
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
    pload = {'username':'Olivia','password':'123'}
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
	
    
    