import time
import json
import boto3
from boto3.dynamodb.conditions import Key

def update_action(table, order_id):
    response = table.update_item(
        Key={
            'order_id': order_id
        },
        UpdateExpression="set init_click_date = :r",
        ExpressionAttributeValues={
            ':r': int(time.time()),
        },
        ReturnValues="UPDATED_NEW"
    )
    print(response)

def lambda_handler(event, context):
    print(event)
    
    order_id = event['order_id']
    
    #write data to dynamo
    dynamo_client = boto3.resource('dynamodb')
    order_table = dynamo_client.Table('order_details')
    
    resp = order_table.query(
        # Add the name of the index you want to use in your query.
        IndexName="order_id-index",
        KeyConditionExpression=Key("order_id").eq(order_id),
    )
    
    order_data = resp['Items'][0]
    rest_number = resp['Items'][0]['restaurant_number']
    
    rest_table = dynamo_client.Table('restaurant_details')
    resp = rest_table.query(KeyConditionExpression=Key('restaurant_number').eq(rest_number))
    rest_data = resp['Items'][0]
    
    response_body = {
        "restaurant_name":rest_data['restaurant_name'],
        "order_items": order_data['order_items'],
        "order_svc": order_data['delivery_service'],
        "customer_name": order_data['person_name'],
        "yelp_link": rest_data['yelp_link'],
        "google_link": rest_data['google_link'],
        "ot_link": rest_data['opentable_link']
        }
    
    #change user_action data
    action_table = dynamo_client.Table('user_action')
    update_action(action_table, order_id)
    
    return {
        'statusCode': 200,
        'body': response_body
    }