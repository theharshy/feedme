import json
import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.types import Binary
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
        rest_number = 'RESTAURANT-ID'
        
    #access message data 
    # rest_number = event["restaurant_id"]
    dynamo_client = boto3.resource('dynamodb')
    order_table = dynamo_client.Table('order_details')
    
    resp = order_table.query(KeyConditionExpression=Key('restaurant_number').eq(rest_number), ScanIndexForward = False)
    order_data = resp['Items']
    reviews_list = []
    for order in order_data:
        
        user_table = dynamo_client.Table('user_action')
        resp = user_table.query(KeyConditionExpression=Key('order_id').eq(order["order_id"]))
        user_response = str(resp['Items'][0].get('init_click_date', "No"))
        if(user_response != "No"):
            user_response = "Yes"
        
        new_order = {
            "customer_name": order["person_name"],
            "customer_number": order["person_number"],
            "delivery_service": order["delivery_service"],
            "order_date": time.strftime('%Y-%m-%d %H:%M', time.localtime(order['order_date'])),
            "response_state": user_response,
            "order_id": order["order_id"],
            "restaurant_name": order["restaurant_name"]
        }
        
        reviews_list.append(new_order)
    
    rest_table = dynamo_client.Table('restaurant_details')
    resp = rest_table.query(KeyConditionExpression=Key('restaurant_number').eq(rest_number))
    restaurant_name = resp['Items'][0]['restaurant_name']
    
    #format response
    
    response_body = {
        "rest_name": restaurant_name,
        "reviews": reviews_list
    }
    
    return {
        'statusCode': 200,
        'body': response_body
    }
