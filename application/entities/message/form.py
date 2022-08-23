from django import forms
from .model import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('notification_id', 'client_id', 'sending_datetime', 'is_send')
