#!/usr/bin/env python
# -*- coding:utf-8 -*-

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

secret_id = 'AKIDaz81e05tPecJkvpTqwqTqypQknZ4IH1U'  # 替换为用户的 secretId
secret_key = 'DApDKAk36sNaMrHTP5UcU6RVIq77rQkn'  # 替换为用户的 secretKey

region = 'ap-beijing'  # 替换为用户的 Region

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)

client = CosS3Client(config)

response = client.upload_file(
    Bucket='linyin-1309571620',
    LocalFilePath='code.png',  # 本地文件的路径
    Key='p1.png'  # 上传到桶之后的文件名
)
print(response['ETag'])