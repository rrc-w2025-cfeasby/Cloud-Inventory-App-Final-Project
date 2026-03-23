import boto3
import json

def lambda_handler(event, context):
    """
    Get All Inventory Items - GET
    """
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('Inventory')

    try:
        response = table.scan()
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