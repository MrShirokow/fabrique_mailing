from rest_framework import serializers

from application.entities.message import Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for message entity
    """
    class Meta:
        model = Message
        fields = ('id', 'notification', 'client', 'sending_datetime', 'is_sending')
