from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    phone_number = PhoneNumberField()
    mobile_operator_code = models.IntegerField()
    tag = models.CharField(max_length=10)
    time_zone = models.TimeField()
