# Generated by Django 3.2.9 on 2022-02-27 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracer', '0002_auto_20220222_1920'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wiki',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
                ('content', models.TextField(verbose_name='内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('depth', models.SmallIntegerField(default=1, verbose_name='深度')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='tracer.wiki', verbose_name='父文章')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracer.project', verbose_name='项目')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
        ),
    ]