import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

if os.environ['IS_OFFLINE'] == 'true':
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url='http://localhost:8000/')
else:
    dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('Orders')


def writeToDynamo(event, context):
    logger.info('Generating new DynamoDB record')

    order_id = json.loads(event["body"]).get("orderID")
    merchant_id = json.loads(event["body"]).get("merchantID")
    item_name = json.loads(event["body"]).get("itemName")

    entry = {
        "orderID": order_id,
        "merchantID": merchant_id,
        "itemName": item_name
    }

    table.put_item(Item=entry)

    response = {
        "statusCode": 200,
        "body": json.dumps(entry)
    }

    return response
