# stackies-app-api

## AWS SAMを使ったAWSサーバーレスサービスのローカル実行方法
https://rooter.jp/programming/python/aws-sam/

## 以下、最初だけ

```
$ docker network create lambda-local
# AWS CLI での Amazon DynamoDB の使用 | https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-services-dynamodb.html
テーブルの作成
$ aws dynamodb create-table --table-name members \
  --attribute-definitions AttributeName=name,AttributeType=S \
  --key-schema AttributeName=name,KeyType=HASH  \
  --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
  --endpoint-url "http://localhost:8000"

$ aws dynamodb create-table --table-name technologies \
  --attribute-definitions AttributeName=name,AttributeType=S AttributeName=category,AttributeType=S \
  --key-schema AttributeName=name,KeyType=HASH AttributeName=category,KeyType=RANGE  \
  --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
  --endpoint-url "http://localhost:8000"
  
$ aws dynamodb create-table --table-name experience_technologies \
  --attribute-definitions AttributeName=name,AttributeType=S AttributeName=user_id,AttributeType=S \
  --key-schema AttributeName=name,KeyType=HASH AttributeName=user_id,KeyType=RANGE  \
  --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
  --endpoint-url "http://localhost:8000"
テーブルの作成確認
$ aws dynamodb list-tables --endpoint-url 'http://localhost:8000'
```

## 日々の開発

```
# localのdynamodbコンテナ起動
$ docker-compose up -d
# API Gatewayのローカル起動
$ sam local start-api --docker-network lambda-local --skip-pull-image --debug
# データ登録(dynamodb SDK)
$ aws dynamodb put-item \
    --table-name technologies \
    --item '{
        "name": {"S": "C#"} ,
        "category": {"S": "1"} 
      }'
# データ登録(REST API)
$ curl "http://localhost:3000/members" -X POST -d '{"name": "fukushima"}'
$ curl "http://localhost:3000/technologies" -X POST -d '{"name": "C#", "category" : "1"}'
$ curl "http://localhost:3000/experience_technology" -X POST -d '{"user_id":"myantyuWorld", "name": "C#", "category" : "1", "level":"3"}'
# 登録できているか確認
$ aws dynamodb scan --table-name members --endpoint-url "http://localhost:8000"
```

## deploy
```
$ cd aws-sam-api
$ sam deploy
```

# 以下不要

## aws-cli
※ // AWS ACCESS KEY等は、Slack#ブックマーク参照
"aws-cli"フォルダは今は使用していません。

