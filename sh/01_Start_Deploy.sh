#!/bin/bash

ACCOUNT_ID=`aws sts get-caller-identity --query Account --output text`
PROJECT="alexachatgpt"

aws s3 mb s3://${PROJECT}-code-${ACCOUNT_ID}

sleep 5

aws s3 cp lambda/alexachatgpt.zip s3://${PROJECT}-code-${ACCOUNT_ID}/lambda/

aws cloudformation create-stack --stack-name StackAlexaChatGPT --template-body file://chatgpt.yaml \
    --capabilities CAPABILITY_NAMED_IAM