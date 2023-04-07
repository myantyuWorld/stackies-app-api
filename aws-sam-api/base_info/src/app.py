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
table = dynamodb.Table('base_info')

def post_handler(event, context):
    # リクエストbody取得
    body = json.loads(event["body"])

    baseinfo = body["data"]["baseinfo"]
    experienceRateInfo = body["data"]["experienceRateInfo"]

    print(baseinfo)
    print(experienceRateInfo)

    user_id = baseinfo["user_id"]
    initial = baseinfo["initial"]
    barthday = baseinfo["birth_date"]
    last_educational_background = baseinfo["last_educational_background"]
    qualification = baseinfo["qualification"]
    self_pr = baseinfo["self_pr"]
    # # db登録
    result = client.put_item(TableName="base_info",
                             Item={
                                 "user_id": {"S": user_id},
                                 "initial": {"S": initial},
                                 "birth_date": {"S": barthday},
                                 "last_educational_background": {"S": last_educational_background},
                                 "qualification": {"S": qualification},
                                 "self_pr": {"S": self_pr},
                             })
    for technology in experienceRateInfo:
        # # db登録
        result = client.put_item(TableName="experience_technologies",
                                 Item={
                                     "user_id": {"S": user_id},
                                     "name": {"S": technology['name']},
                                     "category": {"S": technology['category']},
                                     "level": {"S": str(technology['level'])},
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
    print(res)

    response = {
        "statusCode": 200,
        "body": json.dumps(res['Items'])
    }

    return response
