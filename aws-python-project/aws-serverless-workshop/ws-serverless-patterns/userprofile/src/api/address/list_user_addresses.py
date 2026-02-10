import json
import os
import boto3
from boto3.dynamodb.conditions import Key

# Globals
address_table = os.getenv('TABLE_NAME')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(address_table)

def list_addresses(event, context):
    print(f"Event: {event}")
    user_id = event['requestContext']['authorizer']['claims']['sub']
    print(f"Retrieving addresses for user {user_id}")

    response = table.query(
        KeyConditionExpression=Key('user_id').eq(user_id)
    )
    items = response['Items']
    # remove the user_id property since it should be transparent to the user
    for item in items:
        item.pop("user_id", None)

    print(f"Items: {items}")
    print(f"Found {len(items)} address(es) for user.")
    return items

def lambda_handler(event, context):
    try:
        addresses = list_addresses(event, context)
        response = {
            "statusCode": 200,
            "headers": {},
            "body": json.dumps({
                "addresses": addresses
            })
        }
        return response
    except Exception as err:
        print(f"Error: {err}")
        raise
