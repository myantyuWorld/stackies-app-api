import json
import boto3

# ローカルで開発する場合は、""で良いが、AWSにデプロイする場合は、実際のdynamodbのエンドポイントを指定する必要がある
# TODO : -> endpoint_url不要（削除したら動いた、なぜ？）→ ローカルでの開発時も不要？？
#
# 東京リージョンの場合、「dynamodb.ap-northeast-1.amazonaws.com」
# 参考：https://docs.aws.amazon.com/ja_jp/general/latest/gr/ddb.html
# client = boto3.client('dynamodb', endpoint_url = "http://dynamodb-local:8000")
client = boto3.client('dynamodb')

def get_handler(event, context):
    result = client.scan(TableName="members")
    print(result)
    response = {
        "statusCode": 200,
        "body": json.dumps(result)
    }

    return response