# Generated by Django 3.2.9 on 2022-02-17 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='telephone',
            field=models.CharField(default='null', max_length=11, unique=True),
        ),
    ]