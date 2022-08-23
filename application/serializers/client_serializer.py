from rest_framework import serializers

from application.entities.client.model import Client


class ClientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'phone_number', 'tag', 'mobile_operator_code', 'time_zone')
