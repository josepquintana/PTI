#############################################################################################################################################################
#############################################################################################################################################################

import ssl
import json
import hashlib
import requests
from flask import Flask, jsonify, request, redirect, make_response, abort, url_for, render_template, send_from_directory
from flask_cors import CORS
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
 
# Flask configuration
app = Flask(__name__, template_folder='www/', static_url_path='', static_folder='www/')
app.config["DEBUG"] = True
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
# app.config['SERVER_NAME'] = website_url 

# Set servers IP address
backend_srv = "10.4.41.142"
frontend_srv = "10.4.41.181" # current Flask

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
    res = requests.get('http://' + backend_srv + '/api/v1/bids/list')
    return res.text, res.status_code


@app.route('/run/list_bid_by_id/<bid_id>', methods=['GET'])
def run_list_bid_by_id(bid_id):  
    res = requests.get('http://' + backend_srv + '/api/v1/bids/list/id/' + bid_id)
    return res.text, res.status_code
    
  
@app.route('/run/create_new_bid', methods=['POST'])
def run_create_new_bid():
    buy_amount = request.form.get("buy_amount", type = str)
    buy_currency = request.form.get("buy_currency", type = str)
    sell_amount = request.form.get("sell_amount", type = str)
    sell_currency = request.form.get("sell_currency", type = str)
    API_KEY = request.form.get("API_KEY", type = str)
    
    pload = { 'buy_amount': buy_amount, 'buy_currency': buy_currency, 'sell_amount': sell_amount, 'sell_currency': sell_currency, 'API_KEY': API_KEY }
    res = requests.post('http://' + backend_srv + '/api/v1/bids/new', data = pload)
    return res.text, res.status_code
  
  
@app.route('/run/block_bid/<bid_id>', methods=['GET'])
def run_block_bid(bid_id):  
    res = requests.get('http://' + backend_srv + '/api/v1/bids/block/' + bid_id)
    return res.text, res.status_code
    
    
@app.route('/run/unblock_and_delete_bid/<bid_id>', methods=['GET'])
def run_unblock_and_delete_bid(bid_id):  
    res = requests.get('http://' + backend_srv + '/api/v1/bids/unblock/' + bid_id)
    return res.text, res.status_code
    

@app.route('/run/delete_bid/<bid_id>', methods=['POST'])
def run_delete_bid(bid_id):  
    API_KEY = request.form.get("API_KEY", type = str)
    pload = { 'API_KEY': API_KEY }
    res = requests.post('http://' + backend_srv + '/api/v1/bids/delete/' + bid_id, data = pload)
    return res.text, res.status_code

 
  
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
    res = requests.post('http://' + backend_srv + '/api/v1/users/signup', data = pload)
    
    # Check if signup has been successful
    if res.status_code == 201:
        # Send email to user with account info
        res_json = json.loads(res.text)['data']
        if send_welcome_mail(name, res_json['email'], res_json['account'], res_json['private_key'], res_json['api_key']) is True:
            return jsonify({ 'user': 'registered' }), 201
        else:
            abort(503)
        
    else:
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
    res_post = requests.post('http://' + backend_srv + '/api/v1/users/login', data = pload)
    
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
    
    # Destroy Log In cookie and redirect to login page
    response = make_response(redirect('/login?logout=1'))
    response.delete_cookie("itoken_user_email")
    response.delete_cookie("itoken_user_key")
        
    return response
   
   
@app.route('/run/get_address_from_email/<email>', methods=['GET'])
def run_get_address_from_email(email):  
    res = requests.get('http://' + backend_srv + '/api/v1/users/list/email/' + email)
    if res.status_code == 200:
        return json.loads(res.text)['users'][0]['account'], 200
    else:
        return res.text, res.status_code
     
     
@app.route('/run/get_my_user_account', methods=['GET'])
def run_get_my_user_account():  
    if is_cookie_valid():
        email = request.cookies.get("itoken_user_email")
        if email is None:
            abort(401)
            
        res = requests.get('http://' + backend_srv + '/api/v1/users/list/email/' + email)
        if res.status_code == 200:
            res_json = json.loads(res.text)['users'][0]
            del res_json['password']
            del res_json['api_key']
            return res_json, 200
        else:
            return res.text, res.status_code
            
    else:
        abort(401)
     
  
#############################################################################################################################################################
""" CHECK LOG IN COOKIE VALIDITY """
#############################################################################################################################################################
    
def is_cookie_valid():
    itoken_user_email = request.cookies.get("itoken_user_email")
    itoken_user_key = request.cookies.get("itoken_user_key")
    
    if itoken_user_email is None or itoken_user_key is None:
        return False
    
    pload = { "itoken_user_email": itoken_user_email, "itoken_user_key": itoken_user_key }
    res_post = requests.post('http://' + backend_srv + '/api/v1/users/login/cookie', data = pload)
    
    if res_post.status_code == 200 and json.loads(res_post.text)['user'] == "valid cookie":
        return True
    else:
        return False
    
#############################################################################################################################################################
""" SEND EMAIL """
#############################################################################################################################################################
    
def send_welcome_mail(receiver_name, receiver_email, receiver_account, receiver_private_key, receiver_api_key):

    # Credentials [TODO: Secure]
    email_address = "itoken@josepquintana.me"
    email_password = "*************" 
    
    context = ssl.create_default_context()
    serverSMTP = smtplib.SMTP_SSL("josepquintana.me", "465", context=context)
    serverSMTP.login(email_address, email_password)
	
    message = """\
        <html>
        <div id="pti-server-card" style="max-width:600px;background:#fdeddb;padding:20px;border-radius:10px">
            <div>
                <img src="https://i.imgur.com/Qg4Pzdi.jpg" width="600" height="auto" style="display:block;margin-bottom:37.5px" alt="header" tabindex="0">
            </div>
            <p style="font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:25px;margin:0 0 20px 0;max-width:600px">Hi there <b>{0}</b>,<br><br>Your account has been created successfully. Welcome to the <span style="color:#d47939;font-weight:bold">iToken</span> community<br><br>Below you will find your account information:</p>
            <p style="font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:25px;margin:0 0 20px 15px;max-width:600px"><u>Account email address:</u><br><code style="color:#757575;">{1}</code></p>
            <p style="font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:25px;margin:0 0 20px 15px;max-width:600px"><u>Account address:</u><br><code style="color:#757575;">{2}</code></p>
            <p style="font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:25px;margin:0 0 20px 15px;max-width:600px"><u>Account private key:</u><br><code style="color:#757575;">{3}</code></p>
            <p style="font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:25px;margin:0 0 37.5px 15px;max-width:600px"><u>Account api key:</u><br><code style="color:#757575;">{4}</code></p>
            <p style="font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:25px;margin:0 0 37.5px 0;max-width:600px">Remember to keep your information private!</p>
            <p style="font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:25px;margin:0 0 37.5px 0;max-width:600px">You can login with your credentials by clicking the following link:</p>
            <div style="display:block;max-width:600px;background:#a72020;padding:15px 40px 15px 40px;margin:0 0 37.5px 0;border-radius:50px;color:white;border:solid 1px black;font-size:15px;font-weight:bold;text-align:center;text-decoration:none"><a rel="noopener noreferrer" href="http://{5}/login?name={6}&email={7}" style="font-family:Helvetica,Arial,sans-serif;padding:7.5px 7.5px 7.5px 7.5px;color:white;letter-spacing:3px;vertical-align:baseline;text-decoration:none" target="_blank">ACCESS YOUR ACCOUNT</a></div>
            <table style="margin:0 0 37.5px 0">
                <tbody>
                    <tr>
                        <td style="width:90%">
                            <p style="max-width:600px;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;margin:0;line-height:25px">Thank you and king <span style="color:#d47939;font-weight:bold">regards</span>,<br><br><span style="font-style:italic">iToken Team</span></p>
                        </td>
                        <td style="width:10%"><a rel="noopener noreferrer" href="https://josepquintana.me" target="_blank"><img src="https://josepquintana.me/icons/favicon.png" width="auto" height="64" style="display:block" alt="jq-logo"></a></td>
                    </tr>
                </tbody>
            </table>
        </div>
        </html>
		"""
		
    message = message.format(receiver_name, receiver_email, receiver_account, receiver_private_key, receiver_api_key, receiver_name, receiver_email)
		
    mail = MIMEMultipart()
    mail['From'] = "iToken <" + email_address + ">"
    mail['To'] = receiver_email
    mail['Subject'] = "Welcome to iToken"
    mail.attach(MIMEText(message, "html"))
	
    try:
        serverSMTP.sendmail(mail['From'], mail['To'], mail.as_string())
        return True
		
    except smtplib.SMTPException as e:
        return str(e)
	   
    
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
    
@app.route('/files/abis/Escrow.json', methods=['GET'])
def files_Escrow():
    return send_from_directory("abis", "Escrow.json")
    
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
    
@app.errorhandler(503)
def error_handler_503(error):
	response = { "error": { "code": 503, "message": "Service Unavailable" } }
	return jsonify(response), 503

	
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
	
    
    
