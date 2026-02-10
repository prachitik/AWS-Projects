import json
import os
import boto3
from boto3.dynamodb.conditions import Key

# Globals
favorites_table = os.getenv('TABLE_NAME')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(favorites_table)

def list_favorites(event, context):
    print(f"Event: {event}")

    user_id = event['requestContext']['authorizer']['claims']['sub']
    print(f"Retrieving favorites for user {user_id}")

    response = table.query(
        KeyConditionExpression=Key('user_id').eq(user_id)
    )
    items = response['Items']
    # remove the user_id property since it should be transparent to the user
    for item in items:
        item.pop("user_id", None)

    print(f"Items: {items}")
    print(f"Found {len(items)} favorite(s) for user.")
    return items

def lambda_handler(event, context):
    try:
        favorites = list_favorites(event, context)
        response = {
            "statusCode": 200,
            "headers": {},
            "body": json.dumps({
                "favorites": favorites
            })
        }
        return response
    except Exception as err:
        print(f"Error: {err}")
        raise
