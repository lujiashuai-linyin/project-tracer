# Generated by Django 3.2.9 on 2022-04-25 11:32

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('telephone', models.CharField(default='null', max_length=11, unique=True)),
                ('avatar', models.FileField(default='avatars/default.png', upload_to='avatars/')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AppRequire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='需求名称')),
                ('content', models.TextField(verbose_name='需求内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_user', models.CharField(max_length=16, verbose_name='最近更新')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
        ),
        migrations.CreateModel(
            name='Issues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=80, verbose_name='主题')),
                ('desc', models.TextField(verbose_name='问题描述')),
                ('priority', models.CharField(choices=[('danger', '高'), ('warning', '中'), ('success', '低')], default='danger', max_length=12, verbose_name='优先级')),
                ('status', models.SmallIntegerField(choices=[(1, '新建'), (2, '处理中'), (3, '已解决'), (4, '已忽略'), (5, '待反馈'), (6, '已关闭'), (7, '重新打开')], default=1, verbose_name='状态')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='开始时间')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='结束时间')),
                ('mode', models.SmallIntegerField(choices=[(1, '公开模式'), (2, '隐私模式')], default=1, verbose_name='模式')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('latest_update_datetime', models.DateTimeField(auto_now=True, verbose_name='最后更新时间')),
                ('assign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task', to=settings.AUTH_USER_MODEL, verbose_name='指派')),
                ('attention', models.ManyToManyField(blank=True, related_name='observe', to=settings.AUTH_USER_MODEL, verbose_name='关注者')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='create_problems', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
        ),
        migrations.CreateModel(
            name='PricePolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.SmallIntegerField(choices=[(1, '免费版'), (2, '收费版'), (3, '其他')], default=2, verbose_name='收费类型')),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
                ('price', models.PositiveIntegerField(verbose_name='价格')),
                ('project_num', models.PositiveIntegerField(verbose_name='项目数')),
                ('project_member', models.PositiveIntegerField(verbose_name='项目成员数')),
                ('project_space', models.PositiveIntegerField(help_text='G', verbose_name='单项目空间')),
                ('per_file_size', models.PositiveIntegerField(help_text='M', verbose_name='单文件大小')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='项目名')),
                ('color', models.SmallIntegerField(choices=[(1, '#56b8eb'), (2, '#f28033'), (3, '#ebc656'), (4, '#a2d148'), (5, '#20BFA4'), (6, '#7461c2'), (7, '#20bfa3')], default=1, verbose_name='颜色')),
                ('desc', models.CharField(blank=True, max_length=255, null=True, verbose_name='项目描述')),
                ('use_space', models.BigIntegerField(default=0, help_text='字节', verbose_name='项目已使用空间')),
                ('star', models.BooleanField(default=False, verbose_name='星标')),
                ('join_count', models.SmallIntegerField(default=1, verbose_name='参与人数')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('bucket', models.CharField(max_length=128, verbose_name='cos桶')),
                ('region', models.CharField(max_length=32, verbose_name='cos区域')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
        ),
        migrations.CreateModel(
            name='Wiki',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
                ('content', models.TextField(verbose_name='内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_edit_time', models.DateTimeField(blank=True, null=True, verbose_name='最近修改时间')),
                ('depth', models.SmallIntegerField(default=1, verbose_name='深度')),
                ('last_edit_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edit_user', to=settings.AUTH_USER_MODEL, verbose_name='最近修改人')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='tracer.wiki', verbose_name='父文章')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracer.project', verbose_name='项目')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
        ),
        migrations.CreateModel(
            name='WikiJoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection', models.BooleanField(default=False, verbose_name='收藏')),
                ('editor', models.BooleanField(default=False, verbose_name='编辑')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='参与者')),
                ('wiki', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracer.wiki', verbose_name='wiki')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(choices=[(1, '未支付'), (2, '已支付')], verbose_name='状态')),
                ('order', models.CharField(max_length=64, unique=True, verbose_name='订单号')),
                ('count', models.IntegerField(help_text='0表示无限期', verbose_name='数量（年）')),
                ('price', models.IntegerField(verbose_name='实际支付价格')),
                ('start_datetime', models.DateTimeField(blank=True, null=True, verbose_name='开始时间')),
                ('end_datetime', models.DateTimeField(blank=True, null=True, verbose_name='结束时间')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('price_policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracer.pricepolicy', verbose_name='价格策略')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.BooleanField(default=False, verbose_name='星标')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracer.project', verbose_name='项目')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='参与者')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectInvite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=64, unique=True, verbose_name='邀请码')),
                ('count', models.PositiveIntegerField(blank=True, help_text='空表示无数量限制', null=True, verbose_name='限制数量')),
                ('use_count', models.PositiveIntegerField(default=0, verbose_name='已邀请数量')),
                ('period', models.IntegerField(choices=[(30, '30分钟'), (60, '1小时'), (300, '5小时'), (1440, '24小时')], default=1440, verbose_name='有效期')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='create_invite', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracer.project', verbose_name='项目')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='模块名称')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracer.project', verbose_name='项目')),
            ],
        ),
        migrations.CreateModel(
            name='IssuesType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='类型名称')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracer.project', verbose_name='项目')),
            ],
        ),
        migrations.CreateModel(
            name='IssuesReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_type', models.IntegerField(choices=[(1, '修改记录'), (2, '回复')], verbose_name='类型')),
                ('content', models.TextField(verbose_name='描述')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='create_reply', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('issues', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracer.issues', verbose_name='问题')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracer.issuesreply', verbose_name='回复')),
            ],
        ),
        migrations.AddField(
            model_name='issues',
            name='issues_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracer.issuestype', verbose_name='问题类型'),
        ),
        migrations.AddField(
            model_name='issues',
            name='module',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracer.module', verbose_name='模块'),
        ),
        migrations.AddField(
            model_name='issues',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child', to='tracer.issues', verbose_name='父问题'),
        ),
        migrations.AddField(
            model_name='issues',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracer.project', verbose_name='项目'),
        ),
        migrations.AddField(
            model_name='issues',
            name='require',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracer.apprequire', verbose_name='关联需求'),
        ),
        migrations.CreateModel(
            name='FileRepository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_type', models.SmallIntegerField(choices=[(1, '文件'), (2, '文件夹')], verbose_name='类型')),
                ('name', models.CharField(help_text='文件/文件夹名', max_length=120, verbose_name='文件夹名称')),
                ('key', models.CharField(blank=True, max_length=128, null=True, verbose_name='文件储存在COS中的KEY')),
                ('file_size', models.BigIntegerField(blank=True, help_text='字节', null=True, verbose_name='文件大小')),
                ('file_path', models.CharField(blank=True, max_length=255, null=True, verbose_name='文件路径')),
                ('update_datetime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='tracer.filerepository', verbose_name='父级目录')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracer.project', verbose_name='项目')),
                ('update_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='最近更新者')),
            ],
        ),
        migrations.AddField(
            model_name='apprequire',
            name='project',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='tracer.project', verbose_name='项目'),
        ),
        migrations.CreateModel(
            name='TikTokAutoTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.SmallIntegerField(choices=[(1, 'Android'), (2, 'IOS')], verbose_name='平台')),
                ('version_detail', models.CharField(blank=True, max_length=32, null=True, verbose_name='版本详情')),
                ('task_id', models.IntegerField(verbose_name='任务id')),
                ('test_path', models.CharField(blank=True, max_length=300, null=True, verbose_name='脚本路径')),
                ('event', models.CharField(max_length=16, verbose_name='EVENT')),
                ('test_case_url', models.CharField(max_length=300, verbose_name='埋点url')),
                ('case_id', models.IntegerField(blank=True, null=True, verbose_name='case_id')),
                ('result', models.BooleanField(default=False, verbose_name='测试结果')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='收录时间')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracer.project', verbose_name='项目')),
            ],
            options={
                'ordering': ('-id', '-create_time'),
                'unique_together': {('task_id', 'case_id')},
                'index_together': {('id', 'create_time')},
            },
        ),
    ]
