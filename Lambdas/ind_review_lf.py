import json
import boto3
from boto3.dynamodb.conditions import Key
import time

def lambda_handler(event, context):
    print(event)
    
    client = boto3.client('cognito-idp')
    
    #get user from cognito 
    access_token = event['user_id']
    rest_number = None
    try:
        response = client.get_user(
            AccessToken=access_token
        )
        
        for element in response['UserAttributes']:
            if(element['Name'] == 'phone_number'):
                rest_number = element['Value']
        print("Restaurant number for authentication: ".format(rest_number))
    
    #return issue if cognito does not have user
    except client.exceptions.NotAuthorizedException:
        # return {
        #     'statusCode': 200,
        #     'body': 'Authentication Failure'
        # }
        rest_number = '+14153407579'
        
    cust_number = event['cust_number']
    order_id = event['order_id']
    
    #access message data 
    dynamo_client = boto3.resource('dynamodb')
    msg_table = dynamo_client.Table('chat_messages')
    
    resp = msg_table.query(KeyConditionExpression=Key('customer_number').eq(cust_number))
    msg_data = resp['Items'][0]['messages']
    
    #access order data
    order_table = dynamo_client.Table('order_details')
    
    resp = order_table.query(
        # Add the name of the index you want to use in your query.
        IndexName="order_id-index",
        KeyConditionExpression=Key("order_id").eq(order_id),
    )
    
    order_data = resp['Items'][0]
    
    #format response
    date_string = time.strftime('%Y-%m-%d %H:%M', time.localtime(order_data['order_date']))
    response_body = {
        "delivery_svc": order_data['delivery_service'],
        "order_date": date_string,
        "order_id": order_data['order_id'],
        "customer_name": order_data['person_name'],
        "order_items": order_data['order_items'],
        "order_cost": order_data['order_cost'],
        "delivery_address":order_data['delivery_address'],
        "restaurant_name":order_data['restaurant_name'],
        "rest_number": rest_number,
        "messages": msg_data
    }

    return {
        'statusCode': 200,
        'body': response_body
    }
