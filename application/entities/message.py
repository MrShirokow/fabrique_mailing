from django.db import models

from application.entities.client import Client
from application.entities.notification import Notification


class Message(models.Model):
    notification_id = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='messages')
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages')
    sending_datetime = models.DateTimeField()
    is_send = models.BooleanField(default=False)

    def __str__(self):
        return f'message #{self.id}'

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ['id']
