"""
Reddit-Reader implemented using AWS Lambda and Alexa Skills Kit.
"""

from __future__ import print_function
import json, requests, unidecode, time

SECRETS_FILE = "secrets.json"

# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    if (event['session']['application']['applicationId'] is not
        "amzn1.ask.skill.2ac3515a-250a-4cec-bc0c-82888e433c34"):
        raise ValueError("Invalid Application ID")
    """

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ 
    Called when the user launches the skill without specifying what they want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "YesIntent":
        return share_headlines(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return get_stop_response()
    elif intent_name == "NoIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Hey there, would you like the headlines of the day?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I have not heard your response properly, would you like the news?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_help_response():
    session_attributes = {}
    card_title = "Help"
    speech_output = "If you would like the headlines of the day, say yes. Otherwise, if you would like to exit, say no. So, would you like the news?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I have not heard your response properly, would you like the news?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session)) 


def get_stop_response():
    session_attributes = {}
    card_title = "Stop"
    speech_output = "Am I going too fast? Would you like me to repeat the headlines?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I have not heard your response properly, would you like me to repeat the headlines again?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session)) 


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "See you later! Have a nice day."
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def share_headlines(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    headlines = get_headlines()
    headline_msg = "The current world news headlines are {}".format(headlines)
    speech_output = headline_msg

    reprompt_text = "Would you like me to repeat the headlines?" 

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


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
    titles = "............... ".join([i for i in titles])
    titles += "............... Would you like me to repeat the headlines?" 
    return titles


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'World News',
            'content': output
        },
        'reprompt': {
            'outputSpeech': 
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
