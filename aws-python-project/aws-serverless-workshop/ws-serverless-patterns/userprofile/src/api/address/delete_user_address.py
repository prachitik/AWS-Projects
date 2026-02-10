import os
import boto3

# Globals
address_table = os.getenv('TABLE_NAME')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(address_table)

def delete_address(event, context):
    print(f"Full event: {event}")

    detail = event['detail']
    address_id = detail['addressId']
    user_id = detail['userId']

    if user_id is None or user_id == '':
        raise Exception("User Id could not be found in the incoming event")
    if address_id is None or address_id == '':
        raise Exception("Address Id could not be found in the incoming event")

    print(f"Deleting address {address_id} for user {user_id} from DynamoDb {address_table}")

    table.delete_item(
        Key={
            'user_id': user_id,
            'address_id': address_id
        }
    )
    print(f"Address with ID {address_id} deleted")

def lambda_handler(event, context):
    """Handles the lambda method invocation"""
    try:
        return delete_address(event, context)
    except Exception as err:
        print(f"Error: {err}")
        raise
