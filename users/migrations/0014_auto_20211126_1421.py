# Generated by Django 3.2.9 on 2021-11-26 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20211126_1417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='description',
        ),
        migrations.AddField(
            model_name='post',
            name='desc',
            field=models.TextField(default='', max_length=500),
        ),
    ]
