from django.db import models
from mailing_service.models.notification import Notification
from mailing_service.models.client import Client


class SuccessClient(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='success_clients')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='success_clients', db_index=True)

    class Meta:
        verbose_name = 'success_client'
        verbose_name_plural = 'success_clients'
        ordering = ['id']
        app_label = 'mailing_service'

    def __str__(self) -> str:
        return f'success client #{self.id} from notification #{self.notification}'
