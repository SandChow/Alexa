"""
Reddit-Reader implemented using flask and flask_ask.
"""

from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import logging
import json
import time
import requests
import unidecode

SECRETS_FILE = "secrets.json"

app = Flask(__name__)
ask = Ask(app, '/')
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

def get_headlines():
    with open(SECRETS_FILE) as f:
        secrets = json.load(f)

    login = {'username': secrets['username'],
             'password': secrets['password'],
             'api_type': "json"}

    session = requests.Session()
    session.headers.update({'User-agent': "I am testing Alexa: SandChow"})
    session.post("https://www.reddit.com/api/login", data=login)
    time.sleep(1)
    url = "https://reddit.com/r/worldnews/.json?limit=10"
    html = session.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
    titles = "... ".join([i for i in titles])
    return titles

@ask.launch
def start_skill():
    return question(render_template('welcome_message'))

@ask.intent("YesIntent")
def share_headlines():
    headlines = get_headlines()
    headline_msg = "The current world news headlines are {}".format(headlines)
    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    return statement(render_template('bye_message'))

if __name__ == '__main__':
    app.run(debug=True)
