FROM amazonlinux:2 

RUN yum install -y git wget
# pythonのインストール
RUN amazon-linux-extras install -y python3.8

# エイリアスを設定してコマンド実行時に使用されるバージョンを上書き
RUN echo 'alias python=python3.8' >> ~/.bashrc
RUN source ~/.bashrc

RUN wget https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip
RUN unzip aws-sam-cli-linux-x86_64.zip -d sam_installer
RUN ./sam_installer/install