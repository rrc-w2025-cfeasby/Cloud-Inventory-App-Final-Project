import boto3
import json
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('Inventory')

    item_id = event['pathParameters']['id']

    try:
        response = table.query(
            KeyConditionExpression=Key('item_id').eq(item_id)
        )

        items = response.get('Items', [])

        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps("Item not found")
            }

        clean_item = json.loads(json.dumps(items[0], default=str))

        return {
            'statusCode': 200,
            'body': json.dumps(clean_item)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }