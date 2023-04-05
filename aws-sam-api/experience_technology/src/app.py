import json
from logging import Logger
import boto3
from boto3.dynamodb.conditions import Key, Attr

# ローカルで開発する場合は、""http://dynamodb-local:8000""で良いが、AWSにデプロイする場合は、実際のdynamodbのエンドポイントを指定する必要がある
# TODO : -> endpoint_url不要（削除したら動いた、なぜ？）→ ローカルでの開発時も不要？？
#
# 東京リージョンの場合、「dynamodb.ap-northeast-1.amazonaws.com」
# 参考：https://docs.aws.amazon.com/ja_jp/general/latest/gr/ddb.html
# client = boto3.client('dynamodb', endpoint_url = "http://dynamodb-local:8000")
client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('experience_technology')

# curl "http://localhost:3000/experience_technology" -X POST -d '{"user_id":"myantyuWorld", "name": "C#", "category" : "1", "level":"3"}'
# API Gatewayのルールに則った成功の response を生成する
def create_success_response(body, **kwargs):
    origin  = '*'
    methods = 'GET'

    for k, v in kwargs.items():
        if k == 'origin'  : origin  = v
        if k == 'methods' : methods = v 

    headers = {
        'Access-Control-Allow-Headers' : 'Content-Type',
        'Access-Control-Allow-Origin'  : origin,
        'Access-Control-Allow-Methods' : methods
    }

    # Logger.info(
    #     'return values headers = {}, body = {}, origin = {}, methods = {}'
    #         .format(headers, body, origin, methods)
    # )

    return {
        'isBase64Encoded': False,
        'statusCode'     : 200,
        'headers'        : headers,
        'body'           : json.dumps(body)
    }

# API Gatewayのルールに則った失敗の response を生成する
def create_error_response(body, **kwargs):
    origin  = '*'
    methods = 'GET'

    for k, v in kwargs.items():
        if k == 'origin'  : origin  = v
        if k == 'methods' : methods = v 

    headers = {
        'Access-Control-Allow-Headers' : 'Content-Type',
        'Access-Control-Allow-Origin'  : origin,
        'Access-Control-Allow-Methods' : methods
    }

    return {
        'isBase64Encoded': False,
        'statusCode': 599,
        'headers': headers,
        'body': json.dumps(body)
    }

def post_handler(event, context):
    print('call post ')
    if event['httpMethod'] == 'OPTIONS':
        # logger.info('handle the options method.')
        return create_success_response(
            { 'message': 'successfully: called options method.' },
            methods='GET,OPTIONS,PUT,POST,DELETE'
        )
    # リクエストbody取得
    body = json.loads(event["body"])
    print(body)

    # user_id = body["user_id"]
    # name = body["name"]
    # category = body["category"]
    # level = body["level"]
    # # db登録
    # result = client.put_item(TableName="experience_technology",
    #                          Item={
    #                              "user_id": {"S": user_id},
    #                              "name": {"S": name},
    #                              "category": {"S": category},
    #                              "level": {"S": level},
    #                          })
    headers = {
        'Access-Control-Allow-Headers' : 'Content-Type',
        'Access-Control-Allow-Origin'  : '*',
        'Access-Control-Allow-Methods' : 'POST'
    }
    response = {
        "statusCode": 200,
        'headers': headers,
        # "body": json.dumps(result)
        "body": body
    }

    return response


'''
[{"category": {"S": "1"}, "user_id": {"S": "myantyuWorld"}, "name": {"S": "C#"}, "level": {"S": "3"}}]
'''
# curl "http://localhost:3000/experience_technology"


def get_handler(event, context):
    print(event["queryStringParameters"]["user_id"])
    user_id = event["queryStringParameters"]["user_id"]
    res = table.query(KeyConditionExpression=Key('user_id').eq(user_id))
    print(res)

    headers = {
            'Access-Control-Allow-Headers' : 'Content-Type',
            'Access-Control-Allow-Origin'  : '*',
            'Access-Control-Allow-Methods' : 'GET'
        }
    response = {
        "statusCode": 200,
        'headers': headers,
        "body": json.dumps(res['Items'])
    }

    return response
