import json
import boto3
import ast

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
    response = {
        "statusCode": 200,
        "body": json.dumps(result["Items"])
    }

    return response