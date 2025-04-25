import boto3
import json
from botocore.exceptions import ClientError
from ulid import new as ulid_new

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))

        required_fields = ['name', 'description', 'location_id', 'qty_on_hand', 'price']
        for field in required_fields:
            if field not in body:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': f'Missing required field: {field}'})
                }

        item = {
            'item_id': str(ulid_new()),
            'name': body['name'],
            'description': body['description'],
            'location_id': int(body['location_id']),
            'qty_on_hand': int(body['qty_on_hand']),
            'price': float(body['price'])
        }

        table.put_item(Item=item)

        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'Item added successfully', 'item': item})
        }

    except (ValueError, TypeError):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid input types'})
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
