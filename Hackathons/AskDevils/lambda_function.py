"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
from scipy.misc import derivative

import decimal
import scipy.integrate as integrate
import boto3

DDB = boto3.resource('dynamodb').Table('mathcontext_1')

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
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


# --------------- Functions that control the skill's behavior ------------------

def solveMath(intent, session):
    session_attributes = {}
    card_title = "Welcome"
    ll = intent['slots']['LL']['value']
    ul = intent['slots']['UL']['value']

    if ul is None:
        ul = float('inf')
    if ll is None:
        ll = float('-inf')

    compute = intent['slots']['Compute']['value']
    fn = intent['slots']['function']['value']
    ll = float(ll)
    ul = float(ul)

    def f(x):
        n=1
        m=1
        a=0
        b=0
        c=1
        d=1
        flag = False

        list = fn.split()
        if list[0]=='x':
            flag=True
        #print (list)
        for i in range (1,len(list)):
            if(list[i]==' '):
                continue
            if list[i] == 'x':
                flag = True
                if len(list[i-1]) == 1:
                    n = n*int(list[i-1])
            if (list[i] == 'plus'):
                if(len(list[i-1])==1 and list[i-1] != 'x'):
                    a=a+int(list[i-1])
                if(len(list[i+1])==1 and list[i+1] != 'x'):
                    a=a+int(list[i+1])

            if (list[i] == 'minus'):
                if(len(list[i-1])==1 and list[i-1] != 'x'):
                    b=b-int(list[i-1])
                if(len(list[i+1])==1 and list[i+1] != 'x'):
                    b=b+int(list[i+1])

            if (list[i] == 'multiply'):
                if(len(list[i-1])==1 and list[i-1] != 'x'):
                    n=n*int(list[i-1])
                if(len(list[i+1])==1 and list[i+1] != 'x'):
                    n=n*int(list[i+1])

            if(list[i]=='square' or list[i]=='squared'):
                m=m*2
            if(list[i]=='cube'):
                m=m*3
            if(list[i]=='power'):
                if(len(list[i+1])==1):
                    m=m*int(list[i+1])
                if i+2>=len(list):
                    continue
                else:
                    if list[i+2]=='plus':
                        a=a-int(list[i+1])
                    if list[i+2]=='minus':
                        b=b-int(list[i+1])
                    if list[i+2]=='multiply' and int(list[i+1])!=0:
                        n=n/int(list[i+1])
            
    #print (n, m, a, b, c, d)
        if flag:
            return n*x**m+a-b*c/d
        else:
            return n*0**m+a-b

    
    #solve integration
    if compute in ["integration", "integral", "integration"]:
        result = round(integrate.quad(f, ll, ul)[0],3);
        
    #solve differentiation
    elif compute in ["differentiate", "derivative", "differentiation"]:
        result = round(derivative(f,ul,dx=1e-6) - derivative(f,ll,dx=1e-6),3)


    item = {'Item':{'prevRes': decimal.Decimal(result)}}
    DDB.put_item(**item)
    

  #  session_attributes['prevResult']=result
    result = "The devils have found the answer of " + str(compute) + ". And it is " + str(result)
    speech_output = result
    should_end_session = False
    reprompt_text="I almost heard it. Can you try again?"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

#fn ="2 plus x power 3 multiply 1"

def contextCompute(intent, session):
    session_attributes = {}
    card_title = "Context aware computations"
     #get
    dbitem = {'Item':{'prevRes'}}

    x = float(DDB.get_item(**dbitem))

    DDB.delete_item('Item':{'prevRes':decimal.Decimal(x)})

#    x = float(session['attributes']['prevResult'])
    y = float(intent['slots']['Value']['value'])
    math = intent['slots']['Math']['value']

    if math=='add' or math=='increase':
        result = x+y
    elif math=='subtract' or math=='deduct' or math=='decrease':
        result = x-y
    elif math=='multiply':
        result = x*y
    elif math=='divide' and y!=0:
        result = x/y
    elif math=='divide' and y==0:
        result = 'not defined'

    item = {'Item':{'prevRes': decimal.Decimal(result)}}
    DDB.put_item(**item)
    

    #session_attributes['prevResult']=result
    speech_output = str(result)
    speech_output = "Devil says the new result is "+speech_output
    reprompt_text = "Can you say that again?"
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Skills Kit sample. " \
                    "Please tell me your favorite color by saying, " \
                    "my favorite color is red"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me your favorite color by saying, " \
                    "my favorite color is red."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))



# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
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
    if intent_name=="GetValue":
        return solveMath(intent, session)
    if intent_name=="MakeContextAware":
        return contextCompute(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
