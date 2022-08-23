from django.db import models

from application.entities.client.model import Client
from application.entities.notification.model import Notification


class Message(models.Model):
    notification_id = models.OneToOneField(Notification, on_delete=models.CASCADE, related_name='message')
    client_id = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    sending_datetime = models.DateTimeField()
    is_send = models.BooleanField(default=False)

    def __str__(self):
        return f'message #{self.id}'

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ['id']
