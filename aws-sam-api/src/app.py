import json
import boto3

# ローカルで開発する場合は、""で良いが、AWSにデプロイする場合は、実際のdynamodbのエンドポイントを指定する必要がある
# 東京リージョンの場合、「dynamodb.ap-northeast-1.amazonaws.com」
# 参考：https://docs.aws.amazon.com/ja_jp/general/latest/gr/ddb.html
client = boto3.client('dynamodb', endpoint_url = "http://dynamodb-local:8000")
# client = boto3.client('dynamodb', endpoint_url = "dynamodb.ap-northeast-1.amazonaws.com")

def post_handler(event, context):
    # リクエストbody取得
    body = json.loads(event["body"])
    name = body["name"]
    # db登録
    result = client.put_item(TableName="members", Item={"name": {"S": name}})
    response = {
        "statusCode": 200,
        "body": json.dumps(result)
    }

    return response