import os
import boto3
import json

# Globals
favorites_table = os.getenv('TABLE_NAME')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(favorites_table)

def process_event(event, context):
    print(f"Full event: {event}")
    
    # Handle SQS event
    for record in event['Records']:
        print(f"Processing record: {record}")

        restaurant_id = record['body']
        user_id = record['messageAttributes']['UserId']['stringValue']
        command_name = record['messageAttributes']['CommandName']['stringValue']

        if restaurant_id is None or user_id is None or command_name is None:
            raise Exception("Required command properties are missing")

        if command_name == "AddFavorite":
            add_favorite(user_id, restaurant_id)
        elif command_name == "DeleteFavorite":
            delete_favorite(user_id, restaurant_id)
        else:
            raise Exception(f"Command {command_name} not recognized")

def add_favorite(user_id, restaurant_id):
    """Adds a new favorite restaurant to the user's list"""
    table.put_item(
        Item={
            'user_id': user_id,
            'restaurant_id': restaurant_id
        }
    )
    print(f"Favorite restaurant with ID {restaurant_id} saved for user {user_id}")

def delete_favorite(user_id, restaurant_id):
    """Removes a favorite restaurant from the user's list"""
    print(f"Deleting favorite restaurant {restaurant_id} for user {user_id} from DynamoDb {favorites_table}")

    table.delete_item(
        Key={
            'user_id': user_id,
            'restaurant_id': restaurant_id
        }
    )
    print(f"Favorite restaurant with ID {restaurant_id} deleted")

def lambda_handler(event, context):
    """Entrypoint for Lambda"""
    try:
        return process_event(event, context)
    except Exception as err:
        print(f"Error: {err}")
        raise
