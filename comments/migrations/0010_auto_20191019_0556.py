# Generated by Django 2.2.5 on 2019-10-19 00:26

import comments.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0009_auto_20191019_0553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='slug',
            field=models.SlugField(default=comments.models.generate_id, max_length=35, unique=True),
        ),
        migrations.AlterField(
            model_name='replycomment',
            name='slug',
            field=models.SlugField(default=comments.models.generate_id, max_length=12, unique=True),
        ),
    ]
