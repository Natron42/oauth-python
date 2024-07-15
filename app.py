# copied from https://github.com/piyush-singhal/oauth-python/blob/main/app.py
# this seems the simplest way to authenicate with Google 
# developed on local box and works well.  It pops a browser window open and lets me pick my Google account on my browser
# 
# deploy to Google Shell in the GCP
# I get the expected screen
#   Example of Google Login in Python Flask Application
#   You are not logged in, Click on the below link to sign in with google.
# I click the link and then i get the dreaded 
#   "Access blocked: This app’s request is invalid"
# Any help you can offer would be appreciated.
#
# here is my debug log (with my client-id channged to protect me)
# start the logging.debug
# Hello  line 74
# Hello  line 76
 # * Debugger is active!
 # * Debugger PIN: 127-742-122
# Hello  line 78
# Hello  line 80
# Hello  line 81  Google.base_url    == https://www.googleapis.com/
# Hello  line 82  user_info_endpoint == /oauth2/v2/userinfo
# 127.0.0.1 - - [15/Jul/2024 11:41:41] "GET /?authuser=0 HTTP/1.1" 200 -
# Hello  line 89
# Hello  line 91 my_url_for-->/login/google
# 127.0.0.1 - - [15/Jul/2024 11:42:30] "GET /login HTTP/1.1" 302 -
# client_id = 0000000000000-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com
# Generated new state V18oHjswxgqJML9VgmF7ujpaiLi6KD.
# state = V18oHjswxgqJML9VgmF7ujpaiLi6KD
# redirect URL = https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=0000000000000-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Flogin%2Fgoogle%2Fauthorized&scope=profile+email&state=V18oHjswxgqJML9VgmF7ujpaiLi6KD&prompt=consent


import os
import sys
from flask import Flask, render_template, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
import logging
import json
import json as json_module

app = Flask(__name__)

# Configuration
with open('./credentials.json', 'r') as file:
    json = json.load(file)
client_id     = json['installed']['client_id']
client_secret = json['installed']['client_secret']
secret_key    = os.environ.get("SECRET_KEY") or os.urandom(24)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(message)s')

print("start the logging.debug")
logging.debug("Hello  line 52")

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = secret_key

logging.debug("Hello  line 57")

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

blueprint = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    reprompt_consent=True,
    scope=["profile", "email"]
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/")
def index():
    google_data = None
    user_info_endpoint = '/oauth2/v2/userinfo'
    logging.debug("Hello  line 74")
    if google.authorized:
        logging.debug("Hello  line 76")
        google_data = google.get(user_info_endpoint).json()
        logging.debug("Hello  line 78")

    logging.debug("Hello  line 80")
    logging.debug("Hello  line 81  Google.base_url    == " + google.base_url)
    logging.debug("Hello  line 82  user_info_endpoint == " + user_info_endpoint)
    return render_template('index.j2',
                           google_data=google_data,
                           fetch_url=google.base_url + user_info_endpoint)

@app.route('/login')
def login():
    logging.debug("Hello  line 89")
    my_url_for=url_for('google.login')
    logging.debug("Hello  line 91 my_url_for-->" + my_url_for )
    return redirect(my_url_for)
    #return redirect('/login/google')  #this works

if __name__ == "__main__":
    app.run()