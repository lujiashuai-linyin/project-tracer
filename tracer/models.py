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
    # price_policy = models.ForeignKey(verbose_name='价格策略', to='PricePolicy', to_field='nid', null=False, default=1, on_delete=models.SET_NULL)

    def __str__(self):
        return self.username

class PricePolicy(models.Model):
    """ 价格策略 """
    category_choices = (
        (1, '免费版'),
        (2, '收费版'),
        (3, '其他'),
    )
    category = models.SmallIntegerField(verbose_name='收费类型', default=2, choices=category_choices)
    title = models.CharField(verbose_name='标题', max_length=32)
    price = models.PositiveIntegerField(verbose_name='价格')  # 正整数

    project_num = models.PositiveIntegerField(verbose_name='项目数')
    project_member = models.PositiveIntegerField(verbose_name='项目成员数')
    project_space = models.PositiveIntegerField(verbose_name='单项目空间', help_text='G')
    per_file_size = models.PositiveIntegerField(verbose_name='单文件大小', help_text="M")

    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


    def __str__(self):
        return self.title

class Transaction(models.Model):
    """ 交易记录 """
    status_choice = (
        (1, '未支付'),
        (2, '已支付')
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choice)

    order = models.CharField(verbose_name='订单号', max_length=64, unique=True)  # 唯一索引

    user = models.ForeignKey(verbose_name='用户', to='UserInfo', on_delete=models.CASCADE)
    price_policy = models.ForeignKey(verbose_name='价格策略', to='PricePolicy', on_delete=models.CASCADE)

    count = models.IntegerField(verbose_name='数量（年）', help_text='0表示无限期')

    price = models.IntegerField(verbose_name='实际支付价格')

    start_datetime = models.DateTimeField(verbose_name='开始时间', null=True, blank=True)
    end_datetime = models.DateTimeField(verbose_name='结束时间', null=True, blank=True)

    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class Project(models.Model):
    """ 项目表 """
    COLOR_CHOICES = (
        (1, "#56b8eb"),  # 56b8eb
        (2, "#f28033"),  # f28033
        (3, "#ebc656"),  # ebc656
        (4, "#a2d148"),  # a2d148
        (5, "#20BFA4"),  # #20BFA4
        (6, "#7461c2"),  # 7461c2,
        (7, "#20bfa3"),  # 20bfa3,
    )

    name = models.CharField(verbose_name='项目名', max_length=32)
    color = models.SmallIntegerField(verbose_name='颜色', choices=COLOR_CHOICES, default=1)
    desc = models.CharField(verbose_name='项目描述', max_length=255, null=True, blank=True)

    use_space = models.BigIntegerField(verbose_name='项目已使用空间', default=0, help_text='字节')

    star = models.BooleanField(verbose_name='星标', default=False)

    join_count = models.SmallIntegerField(verbose_name='参与人数', default=1)
    creator = models.ForeignKey(verbose_name='创建者', to='UserInfo', null=True, on_delete=models.SET_NULL)
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    bucket = models.CharField(verbose_name='cos桶', max_length=128)
    region = models.CharField(verbose_name='cos区域', max_length=32)
    def __str__(self):
        return self.name

class ProjectUser(models.Model):
    """ 项目参与者 """
    project = models.ForeignKey(verbose_name='项目', to='Project', on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='参与者', to='UserInfo', on_delete=models.CASCADE)
    star = models.BooleanField(verbose_name='星标', default=False)

    create_datetime = models.DateTimeField(verbose_name='加入时间', auto_now_add=True)

    def __str__(self):
        v = self.project.name + "---" + self.user.username
        return v

class Wiki(models.Model):
    """Wiki"""
    project = models.ForeignKey(verbose_name='项目', to=Project, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='标题', max_length=32)
    content = models.TextField(verbose_name='内容')
    user = models.ForeignKey(verbose_name='创建者', to=UserInfo, null=True, on_delete=models.SET_NULL)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    last_edit_time = models.DateTimeField(verbose_name='最近修改时间', null=True, blank=True)
    last_edit_user = models.ForeignKey(verbose_name='最近修改人', to=UserInfo, null=True, blank=True, on_delete=models.SET_NULL, related_name='last_edit_user')
    depth = models.SmallIntegerField(verbose_name='深度', default=1)
    #自关联
    parent = models.ForeignKey(verbose_name='父文章', to='Wiki', null=True, blank=True, on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return self.title


class WikiJoin(models.Model):
    wiki = models.ForeignKey(verbose_name='wiki', to=Wiki, on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='参与者', to=UserInfo, on_delete=models.CASCADE)
    collection = models.BooleanField(verbose_name='收藏', default=False)
    editor = models.BooleanField(verbose_name='编辑', default=False)
