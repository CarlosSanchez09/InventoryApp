import boto3
import json
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    try:
        id = event['pathParameters']['id']

        # Scan and find full key (id + location_id)
        response = table.scan()
        items = response.get('Items', [])
        item = next((i for i in items if i['id'] == id), None)

        if not item:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Item not found'})
            }

        # Use both keys to delete
        table.delete_item(
            Key={
                'id': item['id'],
                'location_id': item['location_id']
            }
        )

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Item deleted successfully'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Unhandled exception', 'details': str(e)})
        }
