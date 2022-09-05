from rest_framework import serializers

from mailing_service.models.message import Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for message entity
    """
    class Meta:
        model = Message
        fields = ('id', 'notification', 'client', 'is_sending')
