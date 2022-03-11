#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf import settings
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

def create_bucket(bucket=None, region='ap-beijing'):

    config = CosConfig(Region=region, SecretId=settings.COS_SECRET_ID, SecretKey=settings.COS_SECRET_KEY)

    client = CosS3Client(config)

    response = client.create_bucket(
        Bucket=bucket,
        ACL="public-read"  #  private  /  public-read / public-read-write
    )
    cors_config = {
        'CORSRule': [
            {
                'AllowedOrigin': '*',
                'AllowedMethod': ['GET', 'PUT', 'HEAD', 'POST', 'DELETE'],
                'AllowedHeader': "*",
                'ExposeHeader': "*",
                'MaxAgeSeconds': 500
            }
        ]
    }
    client.put_bucket_cors(
        Bucket=bucket,
        CORSConfiguration=cors_config
    )


def upload_file(bucket=None, file_path=None, key=None, region=None):

    config = CosConfig(Region=region, SecretId=settings.COS_SECRET_ID, SecretKey=settings.COS_SECRET_KEY)

    client = CosS3Client(config)

    response = client.upload_file_from_buffer(
        Bucket=bucket,
        Body=file_path,  # 本地文件的路径
        Key=key  # 上传到桶之后的文件名
    )
    return "https://{}.cos.{}.myqcloud.com/{}".format(bucket, region, key)