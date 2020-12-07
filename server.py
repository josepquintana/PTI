#############################################################################################################################################################
#############################################################################################################################################################
"""

============================================================================================================================================================

TODO:

    - API_key for each user
    
    - Check that the newly created bid sell_amount is payable by the owner
    - When a user accepts a bid, check that his own bids are still payable otherwise delete them from the db
    
    
    
    Database is NOT secured!!!!! Can be accessed from outside
   
============================================================================================================================================================   

API endpoints:

/api/v1

    /	

	/bids/
		/new
        /list
            /
            /id/<BID_ID>
            /<BUY_CURRENCY>/<SELL_CURRENCY>
            /blocked
            /unblocked
            /buy/<CURRENCY>[/<MIN_AMOUNT>]
            /sell/<CURRENCY>[/<MIN_AMOUNT>]
            /owner/<USER>
        /block/<BID_ID>
        /unblock/<BID_ID>
        /delete/<BID_ID>
        
	/users
    
============================================================================================================================================================    
    
TESTING:

/test
    /
    /mongo
    /ganache

============================================================================================================================================================        
        
INFORMATION:

/info
    /
    /ip
    /weather
	
============================================================================================================================================================    
    
"""
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
from flask_cors import CORS
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Flask configuration
app = Flask(__name__, template_folder='www/templates', static_url_path='', static_folder='www/static')
app.config["DEBUG"] = True
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
# app.config['SERVER_NAME'] = website_url 

# Flask CORS configuration
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# MongoDB configuration
mongoClient = pymongo.MongoClient("mongodb://10.4.41.142:27017")
pti_Database = mongoClient["DB_PTI"]
bidsCollection = pti_Database["bids"]

# Available Cryptocurrencies
"""
BNC: BarnaToken
FBC: FiberToken
UPC: UpcToken
CTC: CatToken
"""
availableCryptocurrencies = {"BNC", "FBC", "UPC", "CTC"}

#############################################################################################################################################################
""" MAIN WEBSITE """
#############################################################################################################################################################

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        response = { 
            'msg': 'Welcome to the iToken website',
            'org': 'Projecte de Tecnologies de la Informació'
        }
        return jsonify(response), 200
        
    else:
        return render_template("index.html")

#############################################################################################################################################################
""" API ENDPOINTS """
#############################################################################################################################################################

# API -> Root
@app.route('/api/v1', methods=['GET'])
def api_root():
    response = {
        "msg": "API root path",
        "lang": "en",
        "version": "1"
    }
    return jsonify(response), 200

# API -> New bid
@app.route('/api/v1/bids/new', methods=['POST'])
def api_bids_new():
    # Get username/wallet according to the provided API_KEY
    API_KEY = request.form.get("API_KEY", type = str) # Do not set Header application/json !
    username = authenticate_user_api_key(API_KEY)
    
    # Fetch the rest of POST parameters
    buy_amount      = request.form.get("buy_amount", type = int)
    buy_currency    = request.form.get("buy_currency", type = str)
    sell_amount     = request.form.get("sell_amount", type = int)
    sell_currency   = request.form.get("sell_currency", type = str)
    
    # Check if specified parameters are valid
    if buy_amount is None or buy_currency is None or sell_amount is None or sell_currency is None:
        abort(400)
    
    if not is_int(buy_amount) or buy_amount < 0 or not is_int(sell_amount) or sell_amount < 0:
        abort(400)
        
    if not buy_currency in availableCryptocurrencies or not sell_currency in availableCryptocurrencies:
        abort(422)
    
    # Check if the Document already exists in the DB
    checkBid = { "owner": username, "buy_amount": buy_amount, "buy_currency": buy_currency, "sell_amount": sell_amount, "sell_currency": sell_currency }
    if bidsCollection.find(checkBid, { "_id": 1 }).count() > 0:
        abort(409)
    
    # Insert a new Document to the DB
    newBid = { "owner": username, "buy_amount": buy_amount, "buy_currency": buy_currency, "sell_amount": sell_amount, "sell_currency": sell_currency, "blocked": 0 }
    insertedBid = bidsCollection.insert_one(newBid)
       
    response = { 
		'bid': 'created',
		'data': { 
            "id": str(insertedBid.inserted_id), 
            "owner": username, 
            "buy_amount": buy_amount,
            "buy_currency": buy_currency,
            "sell_amount": sell_amount, 
            "sell_currency": sell_currency
        },
        'server_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	}
    
    return jsonify(response), 201

    
# API -> List all bids
@app.route('/api/v1/bids/list', methods=['GET'])
def api_bids_list():
    db_query = bidsCollection.find({}).sort("_id")
    db_query_json = bson.json_util.dumps({ "bids": list(db_query) }, indent = 2)
    response = set_ids_from_objectIds(db_query_json, "bids")
    return response, 200


# API -> List bid with id <BID_ID>
@app.route('/api/v1/bids/list/id/<bid_id>', methods=['GET'])
def api_bids_list_id(bid_id):
    if not bson.objectid.ObjectId.is_valid(bid_id):
        abort(422)
    
    db_query = bidsCollection.find({ "_id": bson.objectid.ObjectId(bid_id) })
    if db_query.count() == 1:
        db_query_json = bson.json_util.dumps({ "bids": list(db_query) }, indent = 2)
        response = set_ids_from_objectIds(db_query_json, "bids")
        return response, 200
    else:
        abort(404)
        

# API -> List bids buying <BUY_CURRENCY> and selling <SELL_CURRENCY>
@app.route('/api/v1/bids/list/<buy_currency>/<sell_currency>', methods=['GET'])
def api_bids_list_buy_sell_currencies(buy_currency, sell_currency):
    if buy_currency in availableCryptocurrencies and sell_currency in availableCryptocurrencies:    
        db_query = bidsCollection.find({ "buy_currency": buy_currency, "sell_currency": sell_currency }).sort("_id")
        db_query_json = bson.json_util.dumps({ "bids": list(db_query) }, indent = 2)
        response = set_ids_from_objectIds(db_query_json, "bids")
        return response, 200
    else:
        abort(422)


# API -> List bids buying <CURRENCY> [at least <MIN_AMOUNT]
@app.route('/api/v1/bids/list/buy/<currency>', defaults={"min_amount": 0}, methods=['GET'] )
@app.route('/api/v1/bids/list/buy/<currency>/<min_amount>', methods=['GET'])
def api_bids_list_buy_currency(currency, min_amount):
    if is_int(min_amount) and int(min_amount) >= 0:
        db_query = bidsCollection.find({ "buy_currency": currency, "buy_amount": { "$gte": int(min_amount) } }).sort("_id")   
        db_query_json = bson.json_util.dumps({ "bids": list(db_query) }, indent = 2)
        response = set_ids_from_objectIds(db_query_json, "bids")
        return response, 200
    else:
        abort(400)


# API -> List bids selling <CURRENCY> [at least <MIN_AMOUNT]
@app.route('/api/v1/bids/list/sell/<currency>', defaults={"min_amount": 0}, methods=['GET'] )
@app.route('/api/v1/bids/list/sell/<currency>/<min_amount>', methods=['GET'])
def api_bids_list_sell_currency(currency, min_amount):
    if is_int(min_amount) and int(min_amount) >= 0:
        db_query = bidsCollection.find({ "sell_currency": currency, "sell_amount": { "$gte": int(min_amount) } }).sort("_id")
        db_query_json = bson.json_util.dumps({ "bids": list(db_query) }, indent = 2)
        response = set_ids_from_objectIds(db_query_json, "bids")
        return response, 200
    else:
        abort(400)


# API -> List bids made by <USER>
@app.route('/api/v1/bids/list/owner/<user>', methods=['GET'])
def api_bids_list_owner(user):
    db_query = bidsCollection.find({ "owner": user }).sort("_id")
    db_query_json = bson.json_util.dumps({ "bids": list(db_query) }, indent = 2)
    response = set_ids_from_objectIds(db_query_json, "bids")
    return response, 200


# API -> Block bid until the blockchain congruences
@app.route('/api/v1/bids/block/<bid_id>', methods=['GET'])
def api_bids_block(bid_id):
    # Check if specified BID_ID is valid
    if not bson.objectid.ObjectId.is_valid(bid_id):
        abort(422)
    
    # Check if the specified BID_ID exists in the DB
    if bidsCollection.find({ "_id": bson.objectid.ObjectId(bid_id) }).count() == 0:
        abort(404)
    
    # Check if that the specified BID_ID is not blocked
    if bidsCollection.find({ "_id": bson.objectid.ObjectId(bid_id), "blocked": 0 }).count() == 0:
        abort(409)
    
    # Update 'blocked' field from DB
    updatedBid = bidsCollection.update_one({ "_id": bson.objectid.ObjectId(bid_id) }, { "$set": { "blocked": 1 } })
    
    if updatedBid.modified_count != 1:
        abort(503)
       
    response = { 
        'bid': 'blocked',
        'data': { 
            "id": bid_id, 
            "blocked": 1
        },
        'server_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return jsonify(response), 200
    
    
# API -> Unlock bid status => Unblocks the BID and Deletes it from the DB since it has been traded
@app.route('/api/v1/bids/unblock/<bid_id>', methods=['GET'])
def api_bids_unblock(bid_id):
    # Check if specified BID_ID is valid
    if not bson.objectid.ObjectId.is_valid(bid_id):
        abort(422)
    
    # Check if the specified BID_ID exists in the DB
    if bidsCollection.find({ "_id": bson.objectid.ObjectId(bid_id) }).count() == 0:
        abort(404)
    
    # Check if that the specified BID_ID is blocked 
    if bidsCollection.find({ "_id": bson.objectid.ObjectId(bid_id), "blocked": 1 }).count() == 0:
        abort(409)
    
    # Delete the Document from the DB
    deletedBid = bidsCollection.delete_one({ "_id": bson.objectid.ObjectId(bid_id) })
       
    if deletedBid.deleted_count != 1:
        abort(503)
       
    response = { 
        'bid': 'unblocked_&_deleted',
        'data': { 
            "id": bid_id
        },
        'server_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return jsonify(response), 200


# API -> Delete bid
@app.route('/api/v1/bids/delete/<bid_id>', methods=['POST'])
def api_bids_delete(bid_id):
    # Get username/wallet according to the provided API_KEY
    API_KEY = request.form.get("API_KEY", type = str) # Do not set Header application/json !
    username = authenticate_user_api_key(API_KEY)
    
    # Check if specified BID_ID is valid
    if not bson.objectid.ObjectId.is_valid(bid_id):
        abort(422)
    
    # Check if the specified BID_ID exists in the DB    
    if bidsCollection.find({ "_id": bson.objectid.ObjectId(bid_id) }).count() == 0:
        abort(404)
        
    # Delete the Document from the DB (only by owner and ownly if not blocked)
    deletedBid = bidsCollection.delete_one({ "_id": bson.objectid.ObjectId(bid_id), "owner": username, "blocked": 0 })
       
    if deletedBid.deleted_count != 1:
        abort(409)
    
    response = { 
        'bid': 'deleted',
        'data': { 
            "id": bid_id, 
            "owner": username
        },
        'server_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return jsonify(response), 200
    

#############################################################################################################################################################
""" API TEST ENDPOINTS """
#############################################################################################################################################################

@app.route('/test', defaults={"dir": ""}, methods=['GET', 'POST'] )
@app.route('/test/1/<dir>', methods=['GET', 'POST'])
def test(dir):
	response = { 
		'test': 'okay',
		'path': '/test/' + dir,
		'method': request.method,
		'GET_var': request.args.get("var", default = "", type = str),
		'POST_var': request.form.get("var", default = "", type = str)
	}
		
	return jsonify(response), 200


@app.route('/test/mongo', methods=['GET'])
def test_mongo():
    return mongoClient.server_info(), 200

#############################################################################################################################################################
""" API INFO ENDPOINTS """
#############################################################################################################################################################

@app.route('/info', methods=['GET'])
def info():
    response = {
        "name": "iToken",
        "subject": "PTI",
        "organization": "UPC",
        "author": "jquintana",
        "lang": "en",
        "version": "v0.1"
    }
	
    return jsonify(response), 200


@app.route('/info/ip', methods=['GET'])
def ip():

	pload = {"requested_with": "xmlhttprequest", "lang": request.args.get("lang", default = "en", type = str)}
	req = requests.post('https://josepquintana.me/ip-tool/run.php', headers = {"referer": "https://josepquintana.me/"}, data = pload)
	if req.status_code == 200:
		response = req.json()
	else:
		response = { 'error': 'Service unavailable' }

	return jsonify(response), 200


@app.route('/info/weather', methods=['GET'])
def weather():
	pload1 = {"requested_with": "xmlhttprequest", "lang": request.args.get("lang", default = "en", type = str)}
	req1 = requests.post('https://josepquintana.me/ip-tool/run.php', headers = {"referer": "https://josepquintana.me/"}, data = pload1)
	if req1.status_code == 200:
		pload2 = {"requested_with": "xmlhttprequest", "lat": req1.json()['lat'], "lon": req1.json()['lon'], "lang": request.args.get("lang", default = "en", type = str)}
		req2 = requests.post('https://josepquintana.me/weather-tool/run.php', headers = {"referer": "https://josepquintana.me/"}, data = pload2)
		
		if req2.status_code == 200:
			response = req2.json()
		else:
			response = { 'error': 'Service 2 unavailable' }
		
	else:
		response = { 'error': 'Service 1 unavailable' }

	return jsonify(response), 200
	

#############################################################################################################################################################
""" SERVE STATIC FILES """
#############################################################################################################################################################

@app.route('/files/abis/BarnaToken.json', methods=['GET'])
def files_BarnaToken():
    return send_from_directory("files/abis", "BarnaToken.json")

@app.route('/files/abis/FiberToken.json', methods=['GET'])
def files_FiberToken():
    return send_from_directory("files/abis", "FiberToken.json")

@app.route('/files/abis/UpcToken.json', methods=['GET'])
def files_UpcToken():
    return send_from_directory("files/abis", "UpcToken.json")

@app.route('/files/abis/CatToken.json', methods=['GET'])
def files_CatToken():
    return send_from_directory("files/abis", "CatToken.json")


#############################################################################################################################################################
""" AUX FUNCTIONS """
#############################################################################################################################################################

def is_int(value):
    try:
        num = int(value)
        return True
    except ValueError:
        return False;
        
        
def set_ids_from_objectIds(db_query_json, root_key):
    response = json.loads(db_query_json)
    for root_element in response[root_key]:
        root_element["id"] = str(root_element["_id"]["$oid"])
        del root_element["_id"]
        
    response = json.dumps(response, indent = 2)
    return response
        

def authenticate_user_api_key(API_KEY):
    # <PROVISIONAL FOR DEV MODE>
    validApiKeys = {
        "0000": "jquintana",
        "1111": "trader1",
        "2222": "trader2",
        "3333": "trader3"
    }
    
    if API_KEY in validApiKeys:
        username = validApiKeys.get(API_KEY)
        print(f"Auth username: ", username)
        return username
    else:
        abort(401)
    # </PROVISIONAL FOR DEV MODE>


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
	
@app.errorhandler(409)
def error_handler_409(error):
	response = { "error": { "code": 409, "message": "Conflict" } }
	return jsonify(response), 409

@app.errorhandler(422)
def error_handler_422(error):
	response = { "error": { "code": 422, "message": "Unprocessable Entity" } }
	return jsonify(response), 422

@app.errorhandler(429)
def error_handler_429(error):
	response = { "error": { "code": 429, "message": "Too Many Requests" } }
	return jsonify(response), 429

	
@app.errorhandler(503)
def error_handler_503(error):
	response = { "error": { "code": 503, "message": "Service Unavailable" } }
	return jsonify(response), 503

	
#############################################################################################################################################################
""" SEND EMAIL """
#############################################################################################################################################################

def send_mail(server_msg_text = "-- EMPTY MESSAGE --"):

	context = ssl.create_default_context()
	serverSMTP = smtplib.SMTP_SSL("josepquintana.me", "465", context=context)
	serverSMTP.login("pti-server@josepquintana.me", "************")
	
	message = """\
		<html>
		<div id="pti-server-card" style="max-width:600px;background:#fdeddb;padding:20px;border-radius:10px">
			<div>
				<img src="https://i.imgur.com/Qg4Pzdi.jpg" width="600" height="auto" style="display:block;margin-bottom:37.5px" alt="header" tabindex="0">
			</div>
			<p style="font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:25px;margin:0 0 37.5px 0;max-width:600px">Hi there <b>Josep</b>,<br><br>You have a message:<br><br><code>{0}</code><br><br>Access the server by clicking the following link:</p>
			<div style="display:block;max-width:600px;background:#a72020;padding:15px 40px 15px 40px;margin:0 0 37.5px 0;border-radius:50px;color:white;border:solid 1px black;font-size:15px;font-weight:bold;text-align:center;text-decoration:none"><a rel="noopener noreferrer" href="http://10.4.41.142" style="font-family:Helvetica,Arial,sans-serif;padding:7.5px 7.5px 7.5px 7.5px;color:white;letter-spacing:3px;vertical-align:baseline;text-decoration:none" target="_blank">ACCESS THE SERVER</a></div>
			<table style="margin:0 0 37.5px 0">
				<tbody>
					<tr>
						<td style="width:90%">
							<p style="max-width:600px;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;margin:0;line-height:25px">Thank you and king <span style="color:#d47939;font-weight:bold">regards</span>,<br><br><span style="font-style:italic">PTI Server Team</span></p>
						</td>
						<td style="width:10%"><a rel="noopener noreferrer" href="https://josepquintana.me" target="_blank"><img src="https://josepquintana.me/icons/favicon.png" width="auto" height="64" style="display:block" alt="jq-logo"></a></td>
					</tr>
				</tbody>
			</table>
		</div>
		</html>
		"""
		
	message = message.format(server_msg_text)
		
	mail = MIMEMultipart()
	mail['From'] = "PTI-Server <pti-server@josepquintana.me>"
	mail['To'] = "josepquintana44@gmail.com"
	mail['Subject'] = "Subscription"
	mail.attach(MIMEText(message, "html"))
	
	try:
		serverSMTP.sendmail(mail['From'], mail['To'], mail.as_string())
		response = { 'status': 'sent' }
		
	except smtplib.SMTPException as e:
		response = { 'error': str(e) }
		
	return jsonify(response), 200
	
    
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
	
	
    
#############################################################################################################################################################
#############################################################################################################################################################
"""


@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))
      
  
	
"""	
#############################################################################################################################################################
#############################################################################################################################################################