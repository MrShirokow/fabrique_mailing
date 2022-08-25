from django.db import models


class Notification(models.Model):
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    text = models.TextField(blank=True)
    mailing_filter = models.JSONField()

    def __str__(self):
        return f'notification #{self.id}'

    class Meta:
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'
        ordering = ['id']
        app_label = 'application'
