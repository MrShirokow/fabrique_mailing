from django.db import models


class Notification(models.Model):
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def __str__(self):
        return f'notification #{self.id}'

    class Meta:
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'
        ordering = ['start_datetime']
