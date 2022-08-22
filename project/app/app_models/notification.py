from django.db import models


class Notification(models.Model):
    start_datetime = models.DateTimeField()
    text = models.TextField()
    end_datetime = models.DateTimeField()
