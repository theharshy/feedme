import json
import boto3
from boto3.dynamodb.conditions import Key
import time

def lambda_handler(event, context):
    
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
    
    # return issue if cognito does not have user
    except:
        # return {
        #     'statusCode': 200,
        #     'body': "Authentication Failured"
        # }
        rest_number = '+14153407579'
    print("here" + rest_number)
    # rest_number = '+14153407579'
    #get review growth information for user 
    dynamo_client = boto3.resource('dynamodb')
    agg_table = dynamo_client.Table('restaurant_agg')
    
    review_perf = {
        "Yelp": [("July", 349), ("August", 364), ("September", 386), ("October", 395), ("November", 418), ("December", 430)],
        "GoogleReviews": [("July", 418), ("August", 429), ("September", 452), ("October", 489), ("November", 503), ("December", 540)],
        "OpenTable": [("July", 261), ("August", 297), ("September", 304), ("October", 310), ("November", 327), ("December", 340)]
    }    
    
    rest_perf = {
        "Doordash": [("July", 120), ("August", 120), ("September", 134), ("October", 158), ("November", 120), ("December", 60)],
        "UberEats": [("July", 105), ("August", 119), ("September", 111), ("October", 89), ("November", 130), ("December", 54)],
        "Postmates": [("July", 60), ("August", 60), ("September", 82), ("October", 67), ("November", 89), ("December", 42)],
        "Grubhub": [("July", 50), ("August", 50), ("September", 50), ("October", 50), ("November", 50), ("December", 22)],
        "Seamless": [("July", 94), ("August", 97), ("September", 99), ("October", 142), ("November", 153), ("December", 88)]
    }
    
    order_table = dynamo_client.Table('order_details')
    resp = order_table.query(KeyConditionExpression=Key('restaurant_number').eq(rest_number), ScanIndexForward = False)
    order_data = resp['Items']
    
    door_dash = 0
    u_e = 0
    post = 0
    grub = 0
    seam = 0
    
    reviews_list = []
    x = 0
    for order in order_data:
        if(order['delivery_service'] == "Uber Eats"):
            u_e += 1
        elif(order['delivery_service'] == "DoorDash"):
            door_dash += 1
        elif(order['delivery_service'] == 'Seamless'):
            seam += 1
        elif(order['delivery_service'] == 'Grubhub'):
            grub += 1
        else:
            post += 1
            
        if(x < 20):
            new_order = {
                "customer_name": order["person_name"],
                "delivery_service": order["delivery_service"],
                "order_date": time.strftime('%Y-%m-%d %H:%M', time.localtime(order['order_date'])),
                "order_id": order["order_id"],
                "restaurant_name": order["restaurant_name"]
            }
            
            reviews_list.append(new_order)
            
        x += 1
            
        

    month_orders = {
        "Doordash": door_dash,
        "UberEats": u_e,
        "Postmates": post,
        "Grubhub": grub,
        "Seamless": seam,
    }
    print("here" + rest_number)
    rest_table = dynamo_client.Table('restaurant_details')
    resp = rest_table.query(KeyConditionExpression=Key('restaurant_number').eq(rest_number))
    restaurant_name = resp['Items'][0]['restaurant_name']
    
    # resp = order_table.query(KeyConditionExpression=Key('restaurant_number').eq(rest_number))
    # order_data = resp['Items']
    # reviews_list = []
    # x = 0
    # for order in order_data:
    #     if(x >= 20):
    #         break
    #     x += 1
        
    #     new_order = {
    #         "customer_name": order["person_name"],
    #         "delivery_service": order["delivery_service"],
    #         "order_date": time.strftime('%Y-%m-%d %H:%M', time.localtime(order['order_date'])),
    #         "order_id": order["order_id"],
    #         "restaurant_name": order["restaurant_name"]
    #     }
        
    #     reviews_list.append(new_order)
    
    response_body = {
        "rest_name": restaurant_name,
        "review_perf": review_perf,
        "rest_perf": rest_perf,
        "order_list": reviews_list,
        "month_orders": month_orders
    }

    
    # TODO implement
    return {
        'statusCode': 200,
        'body': response_body
    }
