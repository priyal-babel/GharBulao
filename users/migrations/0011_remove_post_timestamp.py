# Generated by Django 3.2.9 on 2021-11-24 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_delete_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='timestamp',
        ),
    ]
