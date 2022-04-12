#!/usr/bin/env python
# -*- coding:utf-8 -*-
from concurrent.futures import ThreadPoolExecutor

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import threading

with ThreadPoolExecutor() as pool:
    future = pool.submit()

secret_id = 'AKIDaz81e05tPecJkvpTqwqTqypQknZ4IH1U'   # 替换为用户的 secretId
secret_key = 'DApDKAk36sNaMrHTP5UcU6RVIq77rQkn'  # 替换为用户的 secretKey

region = 'ap-beijing'  # 替换为用户的 Region

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)

client = CosS3Client(config)

response = client.create_bucket(
    Bucket='avatar-1309571620',
    ACL="public-read"  #  private  /  public-read / public-read-write
)