from django.db import models
from django.db.models import Q

from django.apps import apps


class Notification(models.Model):
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    text = models.TextField(blank=True)
    mailing_filter = models.JSONField()

    class Meta:
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'
        ordering = ['id']
        app_label = 'mailing_service'

    def __str__(self):
        return f'notification #{self.id}'

    def save(self, *args, **kwargs):
        model = apps.get_model('mailing_service', 'SuccessClient')
        query = model.objects.filter(Q(notification=self.id))
        if query:
            query.delete()
        super(Notification, self).save(*args, **kwargs)
