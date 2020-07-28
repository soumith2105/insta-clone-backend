# Generated by Django 2.2.5 on 2019-10-17 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0004_comment_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='replycomment',
            name='slug',
            field=models.SlugField(default='KKn9E_SCGNMI', max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='slug',
            field=models.SlugField(default='uZyT7LooZb', max_length=35, unique=True),
        ),
    ]
