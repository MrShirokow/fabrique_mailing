from django.db import models
from django.core.validators import RegexValidator
from timezone_field import TimeZoneField


class Client(models.Model):
    phone_regex = RegexValidator(regex=r'^7\d{10}$', message='Phone number must be in the format: 7XXXXXXXXXX')
    phone_number = models.CharField(validators=[phone_regex], max_length=11, unique=True, blank=False, null=False)
    tag = models.CharField(max_length=10)
    time_zone = TimeZoneField(choices_display='WITH_GMT_OFFSET')

    @property
    def mobile_operator_code(self):
        return self.phone_number[1:4]

    def __str__(self):
        return f'{self.phone_number}'

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'
        ordering = ['id']
