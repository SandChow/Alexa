from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import time
import requests
import unidecode

app = Flask(__name__)
ask = Ask(app, '/reddit_reader')

def get_headlines():
    pass

@app.route('/')
def homepage():
    pass

@ask.launch
def start_skill():
    welcome_message = "Hey there, would you like the headlines of the day?"
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
    headlines = get_headlines()
    headline_msg = "The current world news headlines are {}".format(headlines)
    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text = "See you later then!"
    return statement(bye_text)

if __name__ == '__main__':
    app.run(debug=True)
