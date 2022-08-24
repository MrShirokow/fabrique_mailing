from rest_framework import serializers

from application.entities.notification import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for notification entity
    """
    class Meta:
        model = Notification
        fields = ('id', 'start_datetime', 'end_datetime', 'text')
