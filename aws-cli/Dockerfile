# AWS CLI2 を利用するDockerfile
FROM amazonlinux:2 

# 前提パッケージのインストール
RUN yum install -y unzip less vim which sudo git wget
RUN amazon-linux-extras install -y python3.8

# エイリアスを設定してコマンド実行時に使用されるバージョンを上書き
RUN echo 'alias python=python3.8' >> ~/.bashrc
RUN source ~/.bashrc

# aws cli v2 のインストール
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

RUN wget https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip
RUN unzip aws-sam-cli-linux-x86_64.zip -d sam_installer
RUN ./sam_installer/install

WORKDIR /workdir