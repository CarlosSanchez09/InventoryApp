import boto3
import json
import uuid
from decimal import Decimal
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    try:
        print("RAW EVENT:", json.dumps(event))  # debug log

        body = json.loads(event.get('body', '{}'))

        required_fields = ['name', 'description', 'location_id', 'qty_on_hand', 'price']
        for field in required_fields:
            if field not in body:
                return {
                    'statusCode': 400,
                    'headers': { 'Content-Type': 'application/json' },
                    'body': json.dumps({'error': f'Missing required field: {field}'})
                }

        try:
            location_id = int(body['location_id'])
            qty_on_hand = int(body['qty_on_hand'])
            price = Decimal(str(body['price']))  
        except Exception as cast_err:
            return {
                'statusCode': 400,
                'headers': { 'Content-Type': 'application/json' },
                'body': json.dumps({'error': 'Invalid number format', 'details': str(cast_err)})
            }

        item = {
            'id': str(uuid.uuid4()),
            'name': body['name'],
            'description': body['description'],
            'location_id': location_id,
            'qty_on_hand': qty_on_hand,
            'price': price
        }

        table.put_item(Item=item)

        return {
            'statusCode': 201,
            'headers': { 'Content-Type': 'application/json' },
            'body': json.dumps({'message': 'Item added successfully', 'item': json.loads(json.dumps(item, default=str))})
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'headers': { 'Content-Type': 'application/json' },
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': { 'Content-Type': 'application/json' },
            'body': json.dumps({'error': 'Unhandled exception', 'details': str(e)})
        }
