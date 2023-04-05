import json
import boto3

# ローカルで開発する場合は、""http://dynamodb-local:8000""で良いが、AWSにデプロイする場合は、実際のdynamodbのエンドポイントを指定する必要がある
# TODO : -> endpoint_url不要（削除したら動いた、なぜ？）→ ローカルでの開発時も不要？？
#
# 東京リージョンの場合、「dynamodb.ap-northeast-1.amazonaws.com」
# 参考：https://docs.aws.amazon.com/ja_jp/general/latest/gr/ddb.html
# client = boto3.client('dynamodb', endpoint_url = "http://dynamodb-local:8000")
client = boto3.client('dynamodb')

'''
sam localでCORS対策
https://minerva.mamansoft.net/Notes/sam+local%E3%81%A7CORS%E3%82%92%E8%A7%A3%E6%B6%88
-> https://github.com/aws/aws-sam-cli/issues/323
'''
def options_handler(event, context):
    headers = {
            'Access-Control-Allow-Headers' : 'Content-Type',
            'Access-Control-Allow-Origin'  : '*',
            'Access-Control-Allow-Methods' : 'GET,OPTIONS,PUT,POST,DELETE'
        }
    response = {
        "statusCode": 200,
        'headers': headers,
        "body": ''
    }

    return response

