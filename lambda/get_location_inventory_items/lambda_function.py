import boto3
import json
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('Inventory')

    location_id = int(event['pathParameters']['id'])

    try:
        response = table.query(
            IndexName='GSI_Inventory',
            KeyConditionExpression=Key('item_location_id').eq(location_id)
        )

        items = response.get('Items', [])
        clean_items = json.loads(json.dumps(items, default=str))

        return {
            'statusCode': 200,
            'body': json.dumps(clean_items)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }