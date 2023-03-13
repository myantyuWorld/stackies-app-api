# AWS CLI2 を利用するDockerfile
FROM amazonlinux:2 

# 前提パッケージのインストール
RUN yum install -y unzip less vim which sudo git wget

# aws cli v2 のインストール
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

RUN wget https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip
RUN unzip aws-sam-cli-linux-x86_64.zip -d sam_installer
RUN ./sam_installer/install

# 不要なので、コメントアウト
# aws copilot のインストール
# RUN curl -Lo copilot https://github.com/aws/copilot-cli/releases/latest/download/copilot-linux 
# RUN chmod +x copilot 
# RUN sudo mv copilot /usr/local/bin/copilot 
# RUN copilot --help

WORKDIR /workdir