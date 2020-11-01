#############################################################################################################################################################
#############################################################################################################################################################
"""

TODO:

	endpoint:	10.4.41.142:80/transaction/new
	method: 	POST
	variables:	sender, receiver, amount, price






	API endpoints:
	
	/api/v1 ->
		/transactions ->
			/new
			
		/bids/ ->
			/new
            /list
			
		/users ->
	




"""
#############################################################################################################################################################
#############################################################################################################################################################


import ssl
import json
import smtplib
import requests
import pymongo
from flask import Flask, jsonify, request, render_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Flask configuration
app = Flask(__name__, template_folder='www/templates', static_url_path='', static_folder='www/static')
app.config["DEBUG"] = True
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
# app.config['SERVER_NAME'] = website_url 

# MongoDB configuration
mongoClient = pymongo.MongoClient("mongodb://localhost:27017")
pti_Database = mongoClient["DB_PTI"]
bidsCollection = pti_Database["bids"]

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        response = { 
            'msg': 'Welcome to the <NAME> website',
            'org': 'Projecte de Tecnologies de la Informació'
        }
        return jsonify(response), 200
        
    else:
        return render_template("index.html")

@app.route('/api/v1', methods=['GET'])
def api_root():
    response = {
        "msg": "API root path",
        "lang": "en",
        "version": "1"
    }
    return jsonify(response), 200

# API -> List all bids
@app.route('/api/v1/bids/list', methods=['GET'])
def api_bids_list():
    response = bidsCollection.find()
    return response, 200

# API -> List bids buying <CURRENCY>
@app.route('/api/v1/bids/list/buy/<currency>', methods=['GET'])
def api_bids_list_buy_currency(currency):
    response = bidsCollection.find({ "buy_currency": currency })
    return response, 200

# API -> List bids selling <CURRENCY>
@app.route('/api/v1/bids/list/sell/<currency>', methods=['GET'])
def api_bids_list_sell_currency(currency):
    response = bidsCollection.find({ "sell_currency": currency })
    return response, 200


@app.route('/info', methods=['GET'])
def info():
    response = {
        "name": "<NAME>",
        "subject": "PTI",
        "organization": "UPC",
        "author": "jquintana",
        "lang": "en",
        "version": "v0.1"
    }
	
    return jsonify(response), 200


@app.route('/ip', methods=['GET'])
def ip():

	pload = {"requested_with": "xmlhttprequest", "lang": request.args.get("lang", default = "en", type = str)}
	req = requests.post('https://josepquintana.me/ip-tool/run.php', headers = {"referer": "https://josepquintana.me/"}, data = pload)
	if req.status_code == 200:
		response = req.json()
	else:
		response = { 'error': 'Service unavailable' }

	return jsonify(response), 200



@app.route('/weather', methods=['GET'])
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
	


@app.route('/test', methods=['GET'])
def test_welcome():
	response = { 
		'test': 'okay'
	}
		
	return jsonify(response), 200



@app.route('/test/<path>', methods=['GET', 'POST'])
def test(path):
	response = { 
		'test': 'okay',
		'path': '/test/' + path,
		'method': request.method,
		'GET_var': request.args.get("var", default = "", type = str),
		'POST_var': request.form.get("var", default = "", type = str)
	}
		
	return jsonify(response), 200




#############################################################################################################################################################
""" ERROR HANDLERS """
#############################################################################################################################################################

@app.errorhandler(400)
def error_handler_400(error):
	response = { 'error': '400', 'msg': 'Bad Request' }
	return jsonify(response), 400

@app.errorhandler(401)
def error_handler_401(error):
	response = { 'error': '401', 'msg': 'Unauthorized' }
	return jsonify(response), 401

@app.errorhandler(403)
def error_handler_403(error):
	response = { 'error': '403', 'msg': 'Forbidden' }
	return jsonify(response), 403

@app.errorhandler(404)
def error_handler_404(error):
	response = { 'error': '404', 'msg': 'Not Found' }
	return jsonify(response), 404
	
@app.errorhandler(405)
def error_handler_405(error):
	response = { 'error': '405', 'msg': 'Method Not Allowed' }
	return jsonify(response), 405

@app.errorhandler(429)
def error_handler_429(error):
	response = { 'error': '429', 'msg': 'Too Many Requests' }
	return jsonify(response), 429

	

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
	

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=80, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
	
    app.run(host='0.0.0.0', port=port)
	# app.run()
	
	
    
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