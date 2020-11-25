#############################################################################################################################################################
#############################################################################################################################################################

import ssl
import json
import bson
import smtplib
import requests
import pymongo
from bson import json_util, objectid
from datetime import datetime
from flask import Flask, jsonify, request, abort, render_template, send_from_directory
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Flask configuration
app = Flask(__name__, template_folder='web/', static_url_path='', static_folder='web/')
app.config["DEBUG"] = True
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
# app.config['SERVER_NAME'] = website_url 

#############################################################################################################################################################
""" MAIN WEBSITE """
#############################################################################################################################################################

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")
        

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
	
@app.errorhandler(405)
def error_handler_405(error):
	response = { "error": { "code": 405, "message": "Method Not Allowed" } }
	return jsonify(response), 405
	
@app.errorhandler(406)
def error_handler_406(error):
	response = { "error": { "code": 406, "message": "Not Acceptable" } }
	return jsonify(response), 406

@app.errorhandler(422)
def error_handler_422(error):
	response = { "error": { "code": 422, "message": "Unprocessable Entity" } }
	return jsonify(response), 422

@app.errorhandler(429)
def error_handler_429(error):
	response = { "error": { "code": 429, "message": "Too Many Requests" } }
	return jsonify(response), 429

	
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
	
    
    