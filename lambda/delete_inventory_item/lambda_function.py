import boto3
import json
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    try:
        item_id = event.get('pathParameters', {}).get('id')
        if not item_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing item_id in path'})
            }

        # First, check if item exists
        get_response = table.get_item(Key={'item_id': item_id})
        if 'Item' not in get_response:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Item not found'})
            }

        # Then delete
        table.delete_item(Key={'item_id': item_id})

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Item deleted successfully'})
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
