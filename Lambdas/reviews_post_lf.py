import json
import base64
# from twilio.rest import Client
import json
import os
import urllib
import boto3
from boto3.dynamodb.conditions import Key
from urllib import request, parse

def lambda_handler(event, context):
    TWILIO_SMS_URL = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json"
    TWILIO_ACCOUNT_SID = 'ACe8d1739b569024eb94d016e05dfd308d'
    TWILIO_AUTH_TOKEN = '2aa7d60604b29465c8d29339dbc27305'
    populated_url = TWILIO_SMS_URL.format(TWILIO_ACCOUNT_SID)
    
    print(event)
    
    # event_data = event['data']
    cust_number = event['cust_number']
    rest_number = event['rest_number']
    msg_body = event['msg_body']
    
    #write data to dynamo
    dynamo_client = boto3.resource('dynamodb')
    msg_table = dynamo_client.Table('chat_messages')
    
    resp = msg_table.query(KeyConditionExpression=Key('customer_number').eq(cust_number))
    date = resp['Items'][0]['date']
    update_message(msg_table, cust_number, rest_number, msg_body, date)
    
    #write data to twilio
    populated_url = TWILIO_SMS_URL.format(TWILIO_ACCOUNT_SID)
    post_params = {"To": cust_number, "From": rest_number, "Body": msg_body}
    data = parse.urlencode(post_params).encode()
    req = request.Request(populated_url)
    authentication = "{}:{}".format(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    base64string = base64.b64encode(authentication.encode('utf-8'))
    req.add_header("Authorization", "Basic %s" % base64string.decode('ascii'))
    
    try:
        # perform HTTP POST request
        with request.urlopen(req, data) as f:
            print("Twilio returned {}".format(str(f.read().decode('utf-8'))))
    except Exception as e:
        # something went wrong!
        return e
    
    return {
        'statusCode': 200,
        'body': json.dumps('Message is sent')
    }

def update_message(table, customer_number, rest_number, msg_body, date):
    resp = table.update_item(
        Key={
            'customer_number': customer_number,
            'date': date
        },
        UpdateExpression='SET messages = list_append(messages, :msg_obj)',
        ExpressionAttributeValues={
            ":msg_obj": [
                # {'myObject':
                    {
                        'user': "restaurant",
                        'message': msg_body
                    }
                #}
            ]
        }
    )
    
    print(resp)