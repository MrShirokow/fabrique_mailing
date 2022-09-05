from django.db import models

from mailing_service.models.client import Client
from mailing_service.models.notification import Notification


class Message(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='messages')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_sending = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ['id']
        app_label = 'mailing_service'

    def __str__(self):
        return f'message #{self.id}'
