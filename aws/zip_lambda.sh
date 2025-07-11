#!/bin/bash
rm -rf aws_package
mkdir aws_package
pip install -r requirements.txt -t aws_package/
cp lambda_function.py aws_package/
cd aws_package && zip -r ../lambda_package.zip .
cd ..
