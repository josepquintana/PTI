#############################################################################################################################################################
#############################################################################################################################################################
"""

TODO:

	endpoint:	10.4.41.142:80/transaction/new
	method: 	POST
	variables:	sender, receiver, amount, price

"""
#############################################################################################################################################################
#############################################################################################################################################################


import ssl
import json
import smtplib
import requests
from flask import Flask, jsonify, request, render_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


app = Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False



@app.route('/', methods=['GET'])
def home():
    return "<h1>Projecte de Tecnologies de la Informació</h1><p>Welcome to the <NAME> Web API</p>"



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



@app.route('/random', methods=['GET'])
def random():
    response = [
		{
			"_id": "5f84c8af482ab79cd574aec4",
			"index": 0,
			"guid": "f7efbb42-ed68-4ff8-b89c-5a41d6a8e837",
			"isActive": "false",
			"balance": "$3,602.11",
			"picture": "http://placehold.it/32x32",
			"age": 33,
			"eyeColor": "green",
			"name": "Chandra Gaines",
			"gender": "female",
			"company": "ENTOGROK",
			"email": "chandragaines@entogrok.com",
			"phone": "+1 (901) 504-3070",
			"address": "418 Pooles Lane, Cawood, Kansas, 2564",
			"about": "Labore tempor laboris deserunt veniam duis tempor ex. Eu anim non et anim enim aliquip non deserunt minim et veniam minim. Exercitation et in aliquip consectetur cupidatat elit culpa eiusmod veniam occaecat sunt. Adipisicing laboris adipisicing laboris ex laborum ex qui in. Velit voluptate excepteur consectetur labore nisi. In commodo elit nisi minim aute ex do nulla nostrud. Minim consectetur adipisicing dolor in qui aliqua.\r\n",
			"registered": "2016-09-21T10:56:47 -02:00",
			"latitude": 34.6742,
			"longitude": 109.311574,
			"tags": [
				"ullamco",
				"dolor",
				"anim",
				"est",
				"officia",
				"est",
				"culpa"
			],
			"friends": [
				{
					"id": 0,
					"name": "Melody Morales"
				},
				{
					"id": 1,
					"name": "Amalia Barlow"
				},
				{
					"id": 2,
					"name": "Adele Mendez"
				}
			],
			"greeting": "Hello, Chandra Gaines! You have 3 unread messages.",
			"favoriteFruit": "apple"
		},
		{
			"_id": "5f84c8af36c61c54142581e1",
			"index": 1,
			"guid": "10db26aa-ccbb-4e09-a672-a24de9ebe0ff",
			"isActive": "false",
			"balance": "$3,372.12",
			"picture": "http://placehold.it/32x32",
			"age": 20,
			"eyeColor": "blue",
			"name": "Liza Ferguson",
			"gender": "female",
			"company": "COSMOSIS",
			"email": "lizaferguson@cosmosis.com",
			"phone": "+1 (803) 463-2088",
			"address": "490 Mersereau Court, Newcastle, American Samoa, 3674",
			"about": "Ea pariatur quis fugiat culpa ea ullamco excepteur culpa culpa officia. Labore est veniam exercitation consectetur eiusmod voluptate id. Id laborum elit et commodo tempor veniam cupidatat anim ut ea ut.\r\n",
			"registered": "2019-01-20T02:31:52 -01:00",
			"latitude": -42.570967,
			"longitude": -39.357482,
			"tags": [
				"cupidatat",
				"nostrud",
				"sint",
				"incididunt",
				"aliqua",
				"eiusmod",
				"aliquip"
			],
			"friends": [
				{
					"id": 0,
					"name": "Molina Vargas"
				},
				{
					"id": 1,
					"name": "Joyce Bradley"
				},
				{
					"id": 2,
					"name": "Lowery Holmes"
				}
			],
			"greeting": "Hello, Liza Ferguson! You have 1 unread messages.",
			"favoriteFruit": "banana"
		},
		{
			"_id": "5f84c8af03c7dc33239f7b6b",
			"index": 2,
			"guid": "7d59d982-2927-4561-8cc5-bebcff30b99b",
			"isActive": "false",
			"balance": "$2,540.44",
			"picture": "http://placehold.it/32x32",
			"age": 38,
			"eyeColor": "green",
			"name": "Daniels Deleon",
			"gender": "male",
			"company": "AUTOMON",
			"email": "danielsdeleon@automon.com",
			"phone": "+1 (908) 421-3335",
			"address": "855 Clarendon Road, Cloverdale, Nevada, 814",
			"about": "Veniam dolor velit excepteur labore veniam proident occaecat aliquip. Nulla cupidatat voluptate quis voluptate qui reprehenderit voluptate commodo id amet laboris esse. Magna in qui sit ipsum ut. Cupidatat proident aute id quis sit duis tempor aliqua pariatur esse do aliqua sit.\r\n",
			"registered": "2016-07-28T08:36:51 -02:00",
			"latitude": -69.641406,
			"longitude": 170.403123,
			"tags": [
				"ipsum",
				"aute",
				"aute",
				"aute",
				"minim",
				"cupidatat",
				"aliqua"
			],
			"friends": [
				{
					"id": 0,
					"name": "Sullivan Herrera"
				},
				{
					"id": 1,
					"name": "Lavonne Mcintosh"
				},
				{
					"id": 2,
					"name": "Gray Mills"
				}
			],
			"greeting": "Hello, Daniels Deleon! You have 7 unread messages.",
			"favoriteFruit": "apple"
		},
		{
			"_id": "5f84c8af40d99b7d4eb3206c",
			"index": 3,
			"guid": "f51bc4b9-14b8-47ba-8a4d-17ad6839a159",
			"isActive": "true",
			"balance": "$3,804.48",
			"picture": "http://placehold.it/32x32",
			"age": 37,
			"eyeColor": "blue",
			"name": "Sheri King",
			"gender": "female",
			"company": "EXOTERIC",
			"email": "sheriking@exoteric.com",
			"phone": "+1 (970) 596-2006",
			"address": "133 Ocean Parkway, Bawcomville, Utah, 3814",
			"about": "Aliquip incididunt nulla exercitation magna in sunt ex nisi duis occaecat culpa proident id reprehenderit. Nostrud ipsum voluptate adipisicing et exercitation nostrud qui id. Ad voluptate tempor qui in occaecat. Sit duis id aute velit occaecat elit officia ea. Magna eiusmod ea et Lorem.\r\n",
			"registered": "2019-02-24T07:42:08 -01:00",
			"latitude": -8.067859,
			"longitude": 135.358813,
			"tags": [
				"sunt",
				"aliqua",
				"aliquip",
				"magna",
				"proident",
				"sunt",
				"esse"
			],
			"friends": [
				{
					"id": 0,
					"name": "Margret Castro"
				},
				{
					"id": 1,
					"name": "Foley Koch"
				},
				{
					"id": 2,
					"name": "Carroll Keith"
				}
			],
			"greeting": "Hello, Sheri King! You have 8 unread messages.",
			"favoriteFruit": "strawberry"
		},
		{
			"_id": "5f84c8af8586763804f4129a",
			"index": 4,
			"guid": "b088e143-89f2-4b64-b48d-50dc6dcff326",
			"isActive": "true",
			"balance": "$1,978.22",
			"picture": "http://placehold.it/32x32",
			"age": 26,
			"eyeColor": "brown",
			"name": "Daisy Beck",
			"gender": "female",
			"company": "QUOTEZART",
			"email": "daisybeck@quotezart.com",
			"phone": "+1 (824) 595-2289",
			"address": "490 Bay Parkway, Henrietta, Missouri, 347",
			"about": "Ea cillum magna excepteur ad. Do veniam culpa minim consequat. Nostrud consectetur labore aute ipsum cillum anim excepteur ut cillum et proident in culpa. Ex officia exercitation occaecat est dolor cillum esse laborum do officia.\r\n",
			"registered": "2015-07-03T10:42:55 -02:00",
			"latitude": 61.695545,
			"longitude": 170.208364,
			"tags": [
				"eiusmod",
				"cillum",
				"dolor",
				"proident",
				"irure",
				"Lorem",
				"velit"
			],
			"friends": [
				{
					"id": 0,
					"name": "Roxie Sexton"
				},
				{
					"id": 1,
					"name": "Lakisha Burton"
				},
				{
					"id": 2,
					"name": "Snider Barnes"
				}
			],
			"greeting": "Hello, Daisy Beck! You have 8 unread messages.",
			"favoriteFruit": "strawberry"
		}
	]
	
    return jsonify(response), 200



@app.errorhandler(404)
def page_not_found(error):
	response = { 
		'error': '404',
		'msg': 'Page not found'
	}
	
	return jsonify(response), 404

	

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
	
	
	