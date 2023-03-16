import json
import boto3

client = boto3.client('dynamodb')

def handler(event, context):
    # TODO : 整形して返す
    result = client.scan(TableName="technologies")   

    response = {
        "statusCode": 200,
        "body": json.dumps(result)
    }

    return response