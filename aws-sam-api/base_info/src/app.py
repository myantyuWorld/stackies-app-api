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

# curl "http://localhost:3000/experience_technology" -X POST -d '{"user_id":"myantyuWorld", "name": "C#", "category" : "1", "level":"3"}'


def post_handler(event, context):
    # リクエストbody取得
    body = json.loads(event["body"])
    print(body)

    user_id = body["user_id"]
    initial = body["initial"]
    barthday = body["barthday"]
    last_educational_background = body["last_educational_background"]
    qualification = body["qualification"]
    self_pr = body["self_pr"]
    # db登録
    result = client.put_item(TableName="base_info",
                             Item={
                                 "user_id": {"S": user_id},
                                 "initial": {"S": initial},
                                 "barthday": {"S": barthday},
                                 "last_educational_background": {"S": last_educational_background},
                                 "qualification": {"S": qualification},
                                 "self_pr": {"S": self_pr},
                                 "updated_at": {"S": datetime.datetime.now()},
                             })
    response = {
        "statusCode": 200,
        "body": json.dumps(result)
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

    response = {
        "statusCode": 200,
        "body": json.dumps(res['Items'])
    }

    return response
