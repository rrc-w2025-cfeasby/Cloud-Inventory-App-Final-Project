import boto3
import json
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('Inventory')

    item_id = event['pathParameters']['id']

    try:
        # Query to get the full key (PK + SK)
        response = table.query(
            KeyConditionExpression=Key('item_id').eq(item_id)
        )

        items = response.get('Items', [])
        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps("Item not found")
            }

        item = items[0]

        # Delete using BOTH keys
        table.delete_item(
            Key={
                'item_id': item['item_id'],
                'item_location_id': item['item_location_id']
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps("Item deleted")
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }