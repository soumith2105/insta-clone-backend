# Generated by Django 2.2.5 on 2019-10-19 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0007_auto_20191018_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='slug',
            field=models.SlugField(default='Lls0Emyr0N', max_length=35, unique=True),
        ),
        migrations.AlterField(
            model_name='replycomment',
            name='slug',
            field=models.SlugField(default='7aAI1QmPDIG0', max_length=12, unique=True),
        ),
    ]
