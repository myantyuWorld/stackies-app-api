import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime

# ローカルで開発する場合は、""http://dynamodb-local:8000""で良いが、AWSにデプロイする場合は、実際のdynamodbのエンドポイントを指定する必要がある
# TODO : -> endpoint_url不要（削除したら動いた、なぜ？）→ ローカルでの開発時も不要？？
#
# 東京リージョンの場合、「dynamodb.ap-northeast-1.amazonaws.com」
# 参考：https://docs.aws.amazon.com/ja_jp/general/latest/gr/ddb.html
# client = boto3.client('dynamodb', endpoint_url = "http://dynamodb-local:8000")
client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('project_info')

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


'''
# フロントからのリクエスト
{
  "industries": "1",
  "systemName": "テスト",
  "period": "20230201",
  "businessOverview": "test",
  "language": [
    "C#",
    "Python3.9",
    "Java",
    "TypeScript"
  ],
  "tools": [
    "VSCode"
  ],
  "infra": [
    "AWS Lambda"
  ],
  "workProcess": {
    "rd": true,
    "bd": true,
    "dd": true,
    "cd": true,
    "ut": false,
    "it": false,
    "op": false
  },
  "role": "0"
}
# 上記にプラスして、
user_id, 
project_info_id(システム日付など)を付与
'''
def post_handler(event, context):
    if event['httpMethod'] == 'OPTIONS':
        return create_success_response(
            { 'message': 'successfully: called options method.' },
            methods='GET,OPTIONS,PUT,POST,DELETE'
        )
    
    # リクエストbody取得
    body = json.loads(event["body"])
    print(body)

    user_id = body["user_id"]
    data = body["data"]
    print(data)
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    # # db登録
    result = client.put_item(TableName="project_info",
                                Item={
                                    "user_id": {"S": user_id},
                                    "project_id": {"S":  f'{now:%Y%m%d%H%M%S}' },
                                    "industries": {"S": data['industries']},
                                    "systemName": {"S": data['systemName']},
                                    "period": {"S": data['period']},
                                    "businessOverview": {"S": data['businessOverview']},
                                    "language": {"S": data['language']}, # TODO : 配列のため、エラー
                                    "tools": {"S": data['tools']},# TODO : 配列のため、エラー
                                    "infra": {"S": data['infra']},# TODO : 配列のため、エラー
                                    "workProcess": {"S": data['workProcess']},
                                    "role": {"S": data['role']},
                                })

    response = {
        "statusCode": 200,
        "body": json.dumps(result)
    }

    return response


'''
'''

def get_handler(event, context):
    print(event["queryStringParameters"]["user_id"])
    user_id = event["queryStringParameters"]["user_id"]
    res = table.query(KeyConditionExpression=Key('user_id').eq(user_id))

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
