import boto3
import json
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    try:
        location_id = event.get('pathParameters', {}).get('id')
        if not location_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing location_id in path'})
            }

        response = table.query(
            IndexName='GSI_Location_Inventory',
            KeyConditionExpression=boto3.dynamodb.conditions.Key('location_id').eq(int(location_id))
        )

        items = response.get('Items', [])
        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    except ValueError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid location_id. Must be a number.'})
        }
