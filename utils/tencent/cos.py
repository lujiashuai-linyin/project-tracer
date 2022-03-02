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