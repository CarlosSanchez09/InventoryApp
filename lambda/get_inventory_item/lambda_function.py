import boto3
import json
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    try:
        item_id = event['pathParameters']['id']

        # Query all items and find by item_id only (manual filtering)
        response = table.scan()
        items = response.get('Items', [])

        # Search for match
        item = next((i for i in items if i['item_id'] == item_id), None)

        if not item:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Item not found'})
            }

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(item, default=str)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Unhandled exception', 'details': str(e)})
        }
