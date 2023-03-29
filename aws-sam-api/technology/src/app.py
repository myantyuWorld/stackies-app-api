import json
import boto3
import ast
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('technologies')
client = boto3.client('dynamodb')

'''
[
  {
    "category": {
      "S": "1"
    },
    "name": {
      "S": "typescript"
    }
  },
  {
    "category": {
      "S": "1"
    },
    "name": {
      "S": "C#"
    }
  },
  ...
]
'''
def handler(event, context):
    result = client.scan(TableName="technologies")   
    # res = table.query(KeyConditionExpression=Key('category').eq('1')) # Lang
    headers = {
        'Access-Control-Allow-Headers' : 'Content-Type',
        'Access-Control-Allow-Origin'  : '*',
        'Access-Control-Allow-Methods' : 'GET'
    }
    response = {
        "statusCode": 200,
        'headers': headers,
        "body": json.dumps(result["Items"])
    }

    return response