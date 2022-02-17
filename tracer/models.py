from django.db import models
from django.contrib.auth.models import AbstractUser

class UserInfo(AbstractUser):
    '''
    user message
    '''
    nid = models.AutoField(primary_key=True)
    telephone = models.CharField(max_length=11, null=False, unique=True, default="null")
    avatar = models.FileField(upload_to='avatars/', default='avatars/default.png')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)