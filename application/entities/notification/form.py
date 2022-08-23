from django import forms
from .model import Notification


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ('start_datetime', 'end_datetime')
