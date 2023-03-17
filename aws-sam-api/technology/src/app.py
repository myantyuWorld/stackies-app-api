import json
import boto3

client = boto3.client('dynamodb')

def handler(event, context):
    result = client.scan(TableName="technologies")   

    response = {
        "statusCode": 200,
        "body": json.dumps(result["Items"])
    }

    return response