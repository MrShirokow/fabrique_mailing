import pytz

from rest_framework import serializers

from application.entities.client import Client


class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer for client entity
    """
    time_zone = serializers.ChoiceField(choices=pytz.all_timezones)

    class Meta:
        model = Client
        fields = ('id', 'phone_number', 'tag', 'mobile_operator_code', 'time_zone')
