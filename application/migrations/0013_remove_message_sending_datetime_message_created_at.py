# Generated by Django 4.1 on 2022-08-25 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0012_rename_client_id_message_client_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='sending_datetime',
        ),
        migrations.AddField(
            model_name='message',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
