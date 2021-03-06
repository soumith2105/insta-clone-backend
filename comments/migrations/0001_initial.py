# Generated by Django 2.2.5 on 2019-09-29 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0005_auto_20190928_1312'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('commented_time', models.DateTimeField(auto_now_add=True)),
                ('comment_on', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_on', to='posts.PostFeed')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
