import os
import boto3
import uuid

# Globals
address_table = os.getenv('TABLE_NAME')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(address_table)

def add_address(event, context):
    print(f"Full event: {event}")

    detail = event['detail']
    line1 = detail['line1']
    line2 = detail['line2']
    city = detail['city']
    state_province = detail['stateProvince']
    postal = detail['postal']
    user_id = detail['userId']
    print(f"Saving address for user {user_id}: {line1}, {line2}, {city}, {state_province}, {postal} to DynamoDb {address_table}")

    address_id = str(uuid.uuid4())
    table.put_item(
        Item={
                'address_id': address_id,
                'user_id': user_id,
                'line1': line1,
                'line2': line2,
                'city': city,
                'stateProvince': state_province,
                'postal': postal
            }
        )
    print(f"Address with ID {address_id} saved")
    return address_id

def lambda_handler(event, context):
    """Handles the lambda method invocation"""
    try:
        return add_address(event, context)
    except Exception as err:
        print(f"Error: {err}")
        raise
