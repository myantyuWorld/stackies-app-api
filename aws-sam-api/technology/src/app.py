import json
import boto3

client = boto3.client('dynamodb')

def handler(event, context):
    # TODO : 整形して返す
    result = client.put_item(TableName="technologies")   

    response = {
        "statusCode": 200,
        "body": "hello technology api"
    }

    return response