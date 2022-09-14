import pytz

from rest_framework import serializers

from mailing_service.models.client import Client


def get_default(attr: str, instance):
    if instance is None:
        return None
    return getattr(instance, attr)


class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer for client entity
    """
    time_zone = serializers.ChoiceField(choices=pytz.all_timezones)

    class Meta:
        model = Client
        fields = ('id', 'phone_number', 'tag', 'mobile_operator_code', 'time_zone')

    def validate(self, data):
        phone_number = data.get('phone_number', get_default('phone_number', self.instance))
        mobile_operator_code = data.get('mobile_operator_code',
                                        get_default('mobile_operator_code', self.instance))
        if phone_number[1:4] != str(mobile_operator_code):
            raise serializers.ValidationError({'mobile_operator_code': 'invalid value of mobile operator code'})
        return data
