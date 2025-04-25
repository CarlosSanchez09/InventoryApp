import boto3
import json
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    try:
        location_id = int(event['pathParameters']['id'])

        response = table.scan(
            FilterExpression=Attr('location_id').eq(location_id)
        )

        items = response.get('Items', [])

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'items': items}, default=str)
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Unhandled exception', 'details': str(e)})
        }
