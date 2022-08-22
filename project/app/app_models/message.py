from django.db import models

from project.app.app_models.client import Client
from project.app.app_models.notification import Notification


class Message(models.Model):
    notification_id = models.OneToOneField(Notification, on_delete=models.CASCADE, related_name='message')
    client_id = models.ForeignKey(Client, on_delete=models.SET_NULL)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
