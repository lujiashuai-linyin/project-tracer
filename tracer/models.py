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
    price_policy = models.ForeignKey(verbose_name='价格策略', to='PricePolicy', to_field='nid', null=False, default=1, on_delete=models.SET_NULL)

    def __str__(self):
        return self.username

class PricePolicy(models.Model):
    nid = models.AutoField(primary_key=True)
    tittle = models.CharField(max_length=10, null=False, default='null', unique=True, verbose_name='标题')
    price = models.CharField(max_length=10, null=True, verbose_name='价格/年')
    create_object_count = models.IntegerField(max_length=10, null=False, default=3, verbose_name='创建项目个数')
    object_member = models.IntegerField(max_length=10, null=False, default=2, verbose_name='每个项目成员')
    object_space = models.CharField(max_length=10, null=False, default='20M', verbose_name='每个项目空间')
    single_file = models.CharField(max_length=10, null=False, default='5M', verbose_name='单文件大小')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.tittle

class Transaction(models.Model):

    nid = models.AutoField(primery_key=True)
    status = models.CharField(max_length=10, null=False, default='已支付', verbose_name='交易状态')
    user_id = models.ForeignKey(verbose_name='用户ID', to=UserInfo, to_field='nid', on_delete=models.CASCADE)
    price_id = models.ForeignKey(verbose_name='价格ID', to=PricePolicy, to_field='nid', default=1, on_delete=models.SET_DEFAULT)
    actual_payment = models.CharField(max_length=10, verbose_name='实际支付', null=True, default=0)
    #应当在已支付时，设置开始时间
    create_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间', default='null', )
    count = models.IntegerField(verbose_name='数量', default=0, max_length=10)
    order_number = models.CharField(verbose_name='订单编号', null=False, max_length=32, unique=True)

    def __str__(self):
        return self.order_number

class Object(models.Model):
    nid = models.AutoField(primary_key=True)
    object_name = models.CharField(max_length=32, verbose_name='项目名称', db_index=True)
    description = models.TextField(max_length=255, verbose_name='项目描述')
    color = models.CharField(max_length='7', verbose_name='主题颜色')
    creator_star = models.BooleanField(default=False, verbose_name='星标')
    participation_count = models.IntegerField(verbose_name='参与人数')
    create_number_count = models.IntegerField(verbose_name='创建者数量')
    already_constructed = models.CharField(verbose_name='已使用空间')

    def __str__(self):
        return self.object_name

class Participant(models.Model):
    nid = models.AutoField(primery_key=True)
    object_id = models.ForeignKey(verbose_name='项目ID', to=Object, to_field='nid', on_delete=models.CASCADE)
    user_id = models.ForeignKey(verbose_name='用户ID', to=UserInfo, to_field='nid', on_delete=models.CASCADE)
    participant_star = models.BooleanField(verbose_name='星标', default=False)

    def __str__(self):
        v = self.object_id.object_name + "---" + self.user_id.username
        return v

