from django.db import models
from django.contrib.postgres.fields import ArrayField


class Notification(models.Model):
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    text = models.TextField(blank=True)
    mailing_filter = models.JSONField()
    reached_numbers = ArrayField(models.CharField(max_length=11), default=list, blank=True)

    class Meta:
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'
        ordering = ['id']
        app_label = 'application'

    def __str__(self):
        return f'notification #{self.id}'
