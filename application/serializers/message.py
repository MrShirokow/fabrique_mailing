from rest_framework import serializers

from application.entities.message import Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for message entity
    """
    class Meta:
        model = Message
        fields = ('id', 'notification_id', 'client_id', 'sending_datetime', 'is_sending')
