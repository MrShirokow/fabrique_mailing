from django import forms
from .model import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('phone_number', 'tag', 'time_zone')
