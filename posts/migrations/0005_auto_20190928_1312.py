# Generated by Django 2.2.5 on 2019-09-28 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20190626_0608'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postfeed',
            options={'ordering': ['-published_date']},
        ),
    ]