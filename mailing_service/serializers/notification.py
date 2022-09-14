from rest_framework import serializers

from mailing_service.models.notification import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for notification entity
    """
    class Meta:
        model = Notification
        fields = ('id', 'start_datetime', 'end_datetime', 'text', 'mailing_filter')

    def validate(self, attrs):
        mailing_filter = attrs.get('mailing_filter')
        if mailing_filter is None and self.partial and self.instance:
            return attrs
        elif not isinstance(mailing_filter, dict):
            raise serializers.ValidationError({'mailing_filter': 'filter must be in format `key:value`'})

        tag = mailing_filter.get('tag')
        mobile_operator_code = mailing_filter.get('mobile_operator_code')

        if tag is None and mobile_operator_code is None:
            raise serializers.ValidationError({'mailing_filter': 'filter must contain at least one parameter '
                                                                 'from the list: [tag, mobile_operator_code]'})
        return attrs
