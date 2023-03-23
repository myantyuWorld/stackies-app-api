import json
import boto3

# ローカルで開発する場合は、""http://dynamodb-local:8000""で良いが、AWSにデプロイする場合は、実際のdynamodbのエンドポイントを指定する必要がある
# TODO : -> endpoint_url不要（削除したら動いた、なぜ？）→ ローカルでの開発時も不要？？
#
# 東京リージョンの場合、「dynamodb.ap-northeast-1.amazonaws.com」
# 参考：https://docs.aws.amazon.com/ja_jp/general/latest/gr/ddb.html
# client = boto3.client('dynamodb', endpoint_url = "http://dynamodb-local:8000")
client = boto3.client('dynamodb')

# curl "http://localhost:3000/experience_technology" -X POST -d '{"user_id":"myantyuWorld", "name": "C#", "category" : "1", "level":"3"}'


def post_handler(event, context):
    # リクエストbody取得
    body = json.loads(event["body"])
    print(body)

    user_id = body["user_id"]
    name = body["name"]
    category = body["category"]
    level = body["level"]
    # db登録
    result = client.put_item(TableName="experience_technologies",
                             Item={
                                 "name": {"S": name},
                                 "user_id": {"S": user_id},
                                 "category": {"S": category},
                                 "level": {"S": level},
                             })
    response = {
        "statusCode": 200,
        "body": json.dumps(result)
    }

    return response


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
# curl "http://localhost:3000/experience_technology"


def get_handler(event, context):
    result = client.scan(TableName="experience_technologies")

    response = {
        "statusCode": 200,
        "body": json.dumps(result["Items"])
    }

    return response
