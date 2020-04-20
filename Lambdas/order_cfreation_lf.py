from __future__ import print_function
import json
import boto3
import random, string
from boto3.dynamodb.conditions import Key
import time
import os
import urllib
from urllib import request, parse
import base64

def lambda_handler(event, context):
    for record in event['Records']:
        #order creation details 
        order_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
        body = record['body']
        customer_name = body['cust_name']
        customer_number = body['cust_number']
        restaurant_number = body['rest_number']
        restaurant_name = body['rest_name']
        order_date = int(time.time())
        delivery_address = body['address']
        order_items = body['order_items']
        order_cost = body['order_cost']
        delivery_service = body['delivery_svc']
        
        print(customer_name)
        
        #form chat messages if they don't exist
        
        dynamo_client = boto3.resource('dynamodb')
        msg_table = dynamo_client.Table('chat_messages')
        
        resp = msg_table.query(KeyConditionExpression=Key('customer_number').eq(customer_number))
        
        if(len(resp['Items']) == 0):
            add_message(msg_table, customer_number, restaurant_number)
        
        #form customer details
        cust_det_table = dynamo_client.Table('customer_details')
        
        resp = cust_det_table.query(KeyConditionExpression=Key('phone_number').eq(customer_number))
        
        if(len(resp['Items']) > 0):
            update_cust(cust_det_table, customer_name, order_id, customer_number)
        else:
            add_cust(cust_det_table, customer_name, order_id, customer_number)
        
        
        #form order details
        order_table = dynamo_client.Table('order_details')
        add_order(order_table, delivery_address, delivery_service, order_cost, order_date, order_id, order_items, customer_name, customer_number, restaurant_name, restaurant_number)
        
        #form user action
        action_table = dynamo_client.Table('user_action')
        add_action(action_table, customer_number, order_date, order_id)
        
        #send twilio message with proper link
        TWILIO_SMS_URL = "YOUR-TWILIO-SMS-URL"
        TWILIO_ACCOUNT_SID = 'YOUR-TWILIO-ACCOUNT-SID'
        TWILIO_AUTH_TOKEN = 'YOUR-TWILIO-AUTH-TOKEN'
        populated_url = TWILIO_SMS_URL.format(TWILIO_ACCOUNT_SID)
        
        populated_url = TWILIO_SMS_URL.format(TWILIO_ACCOUNT_SID)
        link = "YOUR-WEBSITE-HOMEPAGE?order_id={}".format(order_id)
        msg_body = "Thanks for choosing {} for your meal, {}. We love to hear from our loyal patrons! Feel free to respond to this text message and we'll get back to you ASAP. We'd for you to leave us a review at: {}".format(restaurant_name, customer_name, link)
        post_params = {"To": customer_number, "From": restaurant_number, "Body": msg_body}
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
    
def add_message(table, customer_number, rest_number):
    
    resp = table.put_item(
       Item={
            'customer_number': customer_number,
            'date': int(time.time()),
            'restaurant_number': rest_number,
            'messages': []
        }
    )
    print(resp)
    
def add_cust(table, customer_name, order_id, customer_number):
    
    resp = table.put_item(
       Item={
            'customer_name': customer_name,
            'order_ids': [order_id],
            'phone_number': customer_number
        }
    )
    print(resp)
    
def update_cust(table, customer_name, order_id, customer_number):
    resp = table.update_item(
        Key={
            'phone_number': customer_number,
            'customer_name': customer_name
        },
        UpdateExpression='SET order_ids = list_append(order_ids, :msg_obj)',
        ExpressionAttributeValues={
            ":msg_obj": [
                # {'myObject':
                    order_id
                #}
            ]
        }
    )
    
def add_order(table, d_address, d_service, o_cost, o_date, o_id, o_items, c_name, c_number, r_name, r_number):
    
    resp = table.put_item(
       Item={
            "delivery_address": d_address,
            "delivery_service": d_service,
            "order_cost": o_cost,
            "order_date": o_date,
            "order_id": o_id,
            "order_items": o_items,
            "person_name": c_name,
            "person_number": c_number,
            "restaurant_name": r_name,
            "restaurant_number": r_number
        }
    )
    print(resp)

def add_action(table, c_number, o_date, o_id):
    
    resp = table.put_item(
       Item={
            'customer_number': c_number,
            'init_click': False,
            'order_date': o_date,
            'order_id': o_id
        }
    )
    print(resp)
    
