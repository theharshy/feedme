from __future__ import print_function
import json
import boto3
from boto3.dynamodb.conditions import Key
import time

def lambda_handler(event, context):
    # TODO implement
    print(event)
    cust_number = '+{}'.format(event['From'][3:])
    rest_number = '+{}'.format(event['To'][3:])
    msg_body = event['Body']
    
    msg_body = msg_body.replace('+',' ')
    
    dynamo_client = boto3.resource('dynamodb')
    msg_table = dynamo_client.Table('chat_messages')
    
    resp = msg_table.query(KeyConditionExpression=Key('customer_number').eq(cust_number))
    
    if(len(resp['Items']) > 0):
        date = resp['Items'][0]['date']
        update_message(msg_table, cust_number, rest_number, msg_body, date)
        
    else:
        add_message(msg_table, cust_number, rest_number, msg_body)
    
    
    return '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'\
           '<Response></Response>'

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
                        'user': "user",
                        'message': msg_body
                    }
                #}
            ]
        }
    )
    
    print(resp)
    
def add_message(table, customer_number, rest_number, msg_body):
    
    resp = table.put_item(
       Item={
            'customer_number': customer_number,
            'date': int(time.time()),
            'restaurant_number': rest_number,
            'messages': [{'message': msg_body, 'user': "user"}]
        }
    )
    print(resp)