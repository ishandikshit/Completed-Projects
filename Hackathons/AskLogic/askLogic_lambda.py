#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import boto3
from time import sleep
from decimal import *


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(
    title,
    output,
    reprompt_text,
    should_end_session,
    ):

    return {
        'outputSpeech': {'type': 'PlainText', 'text': output},
        'card': {'type': 'Simple', 'title': 'SessionSpeechlet - ' \
                 + title, 'content': 'SessionSpeechlet - ' + output},
        'reprompt': {'outputSpeech': {'type': 'PlainText',
                     'text': reprompt_text}},
        'shouldEndSession': should_end_session,
        }


def build_response(session_attributes, speechlet_response):
    return {'version': '1.0', 'sessionAttributes': session_attributes,
            'response': speechlet_response}


# --------------- Functions that control the skill's behavior ------------------

def solveLogicStart(intent, session):
    session_attributes = {}
    card_title = 'Solve Logic Begins'
    speech_output = 'Welcome to Find Logic. Say your first statement'
    createTable()
    should_end_session = False
    reprompt_text = 'I almost heard it. Can you try again?'
    return build_response(session_attributes,
                          build_speechlet_response(card_title,
                          speech_output, reprompt_text,
                          should_end_session))


def solveLogicStatement(intent, session):
    session_attributes = {}
    card_title = 'Solve Logic Statement'

    person1 = intent['slots']['Main_User']
    print(person1['value'])
    person2 = intent['slots']['Secondary_User']
    print(person2['value'])
    relation = intent['slots']['Relationship']['value']

    # if person 1 or 2  = I,Me then it is Einstein

    person1_db = initPerson(person1)
    person2_db = initPerson(person2)
    print('''#####''')
    print(person1_db)
    print('''######''')
    print(person1_db)

    relations = ['elder', 'older', 'fitter', 'more valuable', 'senior', 'bigger', 'faster', 'longer', 'larger', 'greater', 'more mature', 'better']
    relationsOp = ['younger', 'less fitter', 'less valuable', 'junior', 'smaller', 'slower', 'shorter', 'less mature', 'worse']

    if relation in relations:
        if float(person1_db['value']) <= float(person2_db['value']):
            person1_db['value'] = float(person2_db['value']) + 1
    elif relation in relationsOp:

        if float(person2_db['value']) <= float(person1_db['value']):
            person2_db['value'] = float(person1_db['value']) + 1

    putTable(person1_db)
    putTable(person2_db)
    print(person1_db)
    print(person2_db)
    speech_output = 'Ok. Noted. Next statement?'
    should_end_session = False
    reprompt_text = 'I almost heard it. Can you try again?'
    return build_response(session_attributes,
                          build_speechlet_response(card_title,
                          speech_output, reprompt_text,
                          should_end_session))


def solveLogicQuestionName(intent, session):
    session_attributes = {}

    person1 = intent['slots']['Main']['name']
    person2 = intent['slots']['Secodary_User']['name']
    relation = intent['slots']['Relation']
    card_title = 'Solve Logic Statement'
    speech_output = 'Ok. Noted. Next statement?'
    should_end_session = False
    reprompt_text = 'I almost heard it. Can you try again?'
    return build_response(session_attributes,
                          build_speechlet_response(card_title,
                          speech_output, reprompt_text,
                          should_end_session))


def createTable():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.create_table(TableName='FindLogic_33',
                                  KeySchema=[{'AttributeName': 'name',
                                  'KeyType': 'HASH'}],
                                  AttributeDefinitions=[{'AttributeName': 'name'
                                  , 'AttributeType': 'S'}],
                                  ProvisionedThroughput={'ReadCapacityUnits': 10,
                                  'WriteCapacityUnits': 10})
    
    
    table = dynamodb.Table('FindLogic_33')


def putTable(person):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('FindLogic_33')
    person['name'] = person['name'].encode('ascii', 'ignore')
    response = table.get_item(Key={'name': person['name']})
    if 'Item' in response:
        print('found Item = ')
        print(response['Item'])
        table.delete_item(
            Key={
                'name': person['name']
            })
            
    table.put_item(Item={'value': format(float(person['value']), '.15g'
                   ), 'name': person['name']})


def initPerson(person):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('FindLogic_33')
    namee = person['value']
    response = table.get_item(Key={'name': namee})
    if 'Item' in response:
        person_db = response['Item']
        return person_db
    else:

        # print(response)
       # print('Null obj in response')

        person['name'] = namee
        person['value'] = format(0, '.15g')
        return person

    putTable(person)


def solveLogicQuestionRelation(intent, session):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('FindLogic_33')
    relation = intent['slots']['Relation']['value']
    relations = ['eldest', 'largest', 'biggest', 'oldest']
    relationsOp = ['youngest', 'smallest', 'shortest']
    
    if relation in relations:

        speech_output = "The Devils say answer is "+str(findMax())
    else:
        speech_output = "The Devils say answer is "+str(findMin())

    card_title = 'Solve Logic Statement'
#    speech_output = 'Ok. Noted. Next statement?'
    session_attributes = {}
    should_end_session = False
    reprompt_text = 'I almost heard it. Can you try again?'
    return build_response(session_attributes,
                          build_speechlet_response(card_title,
                          speech_output, reprompt_text,
                          should_end_session))


def solveLogicQuestionName(intent, session):

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('FindLogic_33')
    relation = intent['slots']['Relation']['value']
    relations = ['eldest', 'largest', 'biggest', 'oldest']
    relationsOp = ['youngest', 'smallest', 'shortest']

    card_title = 'Solve Logic Statement'
    speech_output = 'Ok. Noted. Next statement?'
    session_attributes = {}
    should_end_session = False
    reprompt_text = 'I almost heard it. Can you try again?'
    return build_response(session_attributes,
                          build_speechlet_response(card_title,
                          speech_output, reprompt_text,
                          should_end_session))

def solveLogicStatementEnd(intent, session):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('FindLogic_33')
    table.delete()
    card_title = 'Solve Logic Statement End'
    speech_output = 'Thank You!'
    session_attributes = {}
    should_end_session = True
    reprompt_text = 'I almost heard it. Can you try again?'
    return build_response(session_attributes,
                          build_speechlet_response(card_title,
                          speech_output, reprompt_text,
                          should_end_session))
##### BOOKS #####

def solveLogicArithmetic(intent, session):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('FindLogic_33')
    card_title = 'Solve Logic Books'
    person = intent['slots']['Name']
    quantity = intent['slots']['Quantity']['value']
    person_db = initPerson2(person, quantity)
#   person_final = processLogicAdd(person, quantity)
    putTable(person_db)
    speech_output = 'Ok. Next statement please.'
    session_attributes = {}
    should_end_session = False
    reprompt_text = 'I almost heard it. Can you try again?'
    return build_response(session_attributes,
                          build_speechlet_response(card_title,
                          speech_output, reprompt_text,
                          should_end_session))

def solveLogicArithmeticExchange(intent, session):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('FindLogic_33')
    card_title = 'Solve Logic Books'
    session_attributes = {}
    should_end_session = False
    reprompt_text = 'I almost heard it. Can you try again?'
    person1 = intent['slots']['Main_User']
    person2 = intent['slots']['Secondary_User']
    quantity = intent['slots']['Quantity']['value']

    person_db1 = initPerson3(person1, quantity, 1)
    person_db2 = initPerson3(person2, quantity, 0)
    if person_db1 == -1 or person_db2 == -1:
        return build_response(session_attributes,
                          build_speechlet_response(card_title,
                          "Wrong Inputs", reprompt_text,
                          should_end_session))
#   person_final = processLogicAdd(person, quantity)
    putTable(person_db1)
    putTable(person_db2)
    speech_output = 'Ok. Next statement please.'
    
    return build_response(session_attributes,
                          build_speechlet_response(card_title,
                          speech_output, reprompt_text,
                          should_end_session))


def solveLogicArithmeticRelativeMore(intent,session):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('FindLogic_33')
    card_title = 'Solve Logic Books'
    session_attributes = {}
    should_end_session = False
    reprompt_text = 'I almost heard it. Can you try again?'
    person1 = intent['slots']['Main_User']
    person2 = intent['slots']['Secondary_User']
    quantity = intent['slots']['Quantity']['value']

    person_db1 = initPerson7(person1)
    person_db2 = initPerson4(person2)
    speech_output = "Ok. Noted. Next Statement?"
    if person_db1 == -1 or person_db2 == -1:
        return build_response(session_attributes,
                          build_speechlet_response(card_title,
                          "Wrong Inputs", reprompt_text,
                          should_end_session))

    person_db1['value'] = float(person_db2['value'])+float(quantity)
    putTable(person_db1)
    return build_response(session_attributes,
                          build_speechlet_response(card_title,
                          speech_output, reprompt_text,
                          should_end_session))

def solveLogicArithmeticRelativeLess(intent,session):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('FindLogic_33')
    card_title = 'Solve Logic Books'
    session_attributes = {}
    should_end_session = False
    reprompt_text = 'I almost heard it. Can you try again?'
    person1 = intent['slots']['Main_User']
    person2 = intent['slots']['Secondary_User']
    quantity = intent['slots']['Quantity']['value']

    person_db1 = initPerson7(person1)
    person_db2 = initPerson4(person2)
    speech_output = "Ok. Noted. Next Statement?"
    if person_db1 == -1 or person_db2 == -1:
        return build_response(session_attributes,
                          build_speechlet_response(card_title,
                          "Wrong Inputs", reprompt_text,
                          should_end_session))

    person_db1['value'] = float(person_db2['value'])-float(quantity)
    putTable(person_db1)
    return build_response(session_attributes,
                          build_speechlet_response(card_title,
                          speech_output, reprompt_text,
                          should_end_session))
    
def solveLogicArithmeticQuestionName(intent, session):

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('FindLogic_33')
    card_title = 'Solve Logic Statement'

    name1 = intent['slots']['Name']['value']
    response = table.get_item(Key={'name': name1})

    print (response)
    if 'Item' in response:
        speech_output = str(name1)+" has "+str(response['Item']['value'])+" "+str(intent['slots']['Things']['value'])
    else:
        speech_output = 'Wrong Question!'

    session_attributes = {}
    should_end_session = False
    reprompt_text = 'I almost heard it. Can you try again?'
    return build_response(session_attributes,
                          build_speechlet_response(card_title,
                          speech_output, reprompt_text,
                          should_end_session))

def solveLogicArithmeticQuestionTotal(intent, session):

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('FindLogic_33')
    card_title = 'Solve Logic Statement Total'

    result=table.scan()
    count =0
    for i in range (0, result['Count']):
            count=float(count)+float(result['Items'][i]['value'])
    speech_output = "Total number of "+str(intent['slots']['Things']['value'])+" are "+str(count)
    session_attributes = {}
    should_end_session = False
    reprompt_text = 'I almost heard it. Can you try again?'
    return build_response(session_attributes,
                          build_speechlet_response(card_title,
                          speech_output, reprompt_text,
                          should_end_session))

def initPerson2(person, quantity):
    quantity = float(quantity)
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('FindLogic_33')
    namee = person['value']
    response = table.get_item(Key={'name': namee})
    if 'Item' in response:
        person_db = response['Item']
        person_db['value'] = quantity
        return person_db
    else:

        # print(response)
       # print('Null obj in response')

        person['name'] = namee
        person['value'] = format(quantity, '.15g')
        return person

    putTable(person)

def initPerson3(person, quantity, op):
    quantity = float(quantity)
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('FindLogic_33')
    namee = person['value']
    response = table.get_item(Key={'name': namee})
    if 'Item' in response:
        person_db = response['Item']
        if op==1:
            person_db['value'] = float(person_db['value'])+quantity
        elif op==0:
            person_db['value'] = float(person_db['value'])-quantity
        return person_db
    else:

        return -1

    putTable(person)

def initPerson4(person):

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('FindLogic_33')
    namee = person['value']
    response = table.get_item(Key={'name': namee})
    if 'Item' in response:
        person_db = response['Item']
        return person_db
    else:
        return -1

def initPerson7(person):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('FindLogic_33')
    namee = person['value']
    response = table.get_item(Key={'name': namee})
    if 'Item' in response:
        person_db = response['Item']
        return person_db
    else:

        # print(response)
       # print('Null obj in response')

        person['name'] = namee
        person['value'] = format(0, '.15g')
        return person

    putTable(person)


def findMin():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('FindLogic_33')
    result=table.scan()
    min =1000
    minloc =1000
    for i in range (0, result['Count']):
        if float(result['Items'][i]['value'])<min:
            min=float(result['Items'][i]['value'])
            minloc = i
    return result['Items'][minloc]['name']

def findMax():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('FindLogic_33')
    result=table.scan()
    max =-10
    maxloc =-10
    for i in range (0, result['Count']):
        if float(result['Items'][i]['value'])>max:
            max=float(result['Items'][i]['value'])
            maxloc = i
    return result['Items'][maxloc]['name']
    
def updateValues(person):

    # TODO

    person['value'] = (person['upper_limit'] + person['lower_limit']) \
        / 2
    putTable(person)


def validatePerson(person):

    # TODO

    if person['upper_limit'] < person['lower_limit']:
        return 'Error'


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = 'Welcome'
    speech_output = \
        'Welcome to the team Sun Devils'

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.

    reprompt_text = \
        'Please tell me your favorite color by saying, my favorite color is red.'
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(card_title,
                          speech_output, reprompt_text,
                          should_end_session))


def handle_session_end_request():
    card_title = 'Session Ended'
    speech_output = \
        'Thank you for trying the Alexa Skills Kit sample. Have a nice day! '

    # Setting this to true ends the session and exits the skill.

    should_end_session = True
    return build_response({}, build_speechlet_response(card_title,
                          speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {'favoriteColor': favorite_color}




# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print('on_session_started requestId='
          + session_started_request['requestId'] + ', sessionId='
          + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print('on_launch requestId=' + launch_request['requestId']
          + ', sessionId=' + session['sessionId'])

    # Dispatch to your skill's launch

    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print('on_intent requestId=' + intent_request['requestId']
          + ', sessionId=' + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers

    if intent_name == 'Logic_Age_Verbal_Start':
        return solveLogicStart(intent, session)
    elif intent_name == 'Logic_Age_Verbal_Statement':
        return solveLogicStatement(intent, session)
    elif intent_name == 'Logic_Age_Verbal_Question_Relation':
        return solveLogicQuestionRelation(intent, session)
    elif intent_name == 'Logic_Age_Verbal_Question_Name':
        return solveLogicStatementName(intent, session)
    elif intent_name == 'Logic_Age_Verbal_End':
        return solveLogicStatementEnd(intent, session)
    elif intent_name == 'Logic_Arthimetic_Statement_Simple':
        return solveLogicArithmetic(intent, session)
    elif intent_name == 'Logic_Arthimetic_Statement_Exchange':
        return solveLogicArithmeticExchange(intent, session)
    elif intent_name == 'Logic_Arthimetic_Statement_Relative_More':
        return solveLogicArithmeticRelativeMore(intent, session)
    elif intent_name == 'Logic_Arthimetic_Statement_Relative_Less':
        return solveLogicArithmeticRelativeLess(intent, session)
    elif intent_name == 'Logic_Arthimetic_Question_By_Name':
        return solveLogicArithmeticQuestionName(intent, session)
    elif intent_name == 'Logic_Arthimetic_Question_Thing_All':
        return solveLogicArithmeticQuestionTotal(intent, session)        
        
    
    elif intent_name == 'AMAZON.HelpIntent':

    # #########

        return get_welcome_response()
    elif intent_name == 'AMAZON.CancelIntent' or intent_name \
        == 'AMAZON.StopIntent':
        return handle_session_end_request()
    else:
        raise ValueError('Invalid intent')


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """

    print('on_session_ended requestId='
          + session_ended_request['requestId'] + ', sessionId='
          + session['sessionId'])


    # add cleanup logic here

# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """

    print('event.session.application.applicationId=' + event['session'
          ]['application']['applicationId'])

    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId'
                           ]}, event['session'])

    if event['request']['type'] == 'LaunchRequest':
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == 'IntentRequest':
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == 'SessionEndedRequest':
        return on_session_ended(event['request'], event['session'])
