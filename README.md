# stackies-app-api

## aws-cli
※ // AWS ACCESS KEY等は、Slack#ブックマーク参照

```
docker-compose run --rm aws-cli-container /bin/bash
sam init --runtime python3.8
```

## AWS SAMを使ったAWSサーバーレスサービスのローカル実行方法
https://rooter.jp/programming/python/aws-sam/

```
$ docker network create lambda-local
$ docker-compose up -d

テーブルの作成
$ aws dynamodb create-table --table-name members \
  --attribute-definitions AttributeName=name,AttributeType=S \
  --key-schema AttributeName=name,KeyType=HASH  \
  --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
  --endpoint-url "http://localhost:8000"

テーブルの作成確認
$ aws dynamodb list-tables --endpoint-url 'http://localhost:8000'

API Gatewayのローカル起動
$ sam local start-api --docker-network lambda-local

データ登録確認
$ curl "http://localhost:3000/members" -X POST -d '{"name": "fukushima"}'

登録できているか確認
$ aws dynamodb scan --table-name members --endpoint-url "http://localhost:8000"



```