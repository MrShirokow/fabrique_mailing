from django.db.models import Count
from django.urls import reverse
from rest_framework import status

from mailing_service.models.message import Message
from mailing_service.serializers.message import MessageSerializer
from mailing_service.serializers.message_stats import serialize_stats, get_stats_dict


def test_message_list_by_notification_200(api_client, general_test_data):
    notification_id = general_test_data['notification_data'][0].id
    url = reverse('message-list-by-notification-view', kwargs={'pk': notification_id})
    serializer_data = MessageSerializer([general_test_data['msg_data'][0]], many=True).data
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['sent_messages'] == serializer_data


def test_message_list_by_notification_404(api_client, general_test_data):
    url = reverse('message-list-by-notification-view', kwargs={'pk': 1})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_message_stats_view(api_client, general_test_data):
    url = reverse('message-stats-view')
    queryset = Message.objects.values(
        'notification_id', 
        'is_sending', 
        'notification__text'
    ).annotate(
        count=Count('is_sending')
    ).values_list(
        'notification_id', 
        'is_sending', 
        'count', 
        'notification__text'
    )
    serializer_data = serialize_stats(get_stats_dict(queryset))
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer_data
