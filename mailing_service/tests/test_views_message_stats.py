import pytest

from django.db.models import Count
from django.urls import reverse
from rest_framework import status

from mailing_service.models.client import Client
from mailing_service.models.message import Message
from mailing_service.models.notification import Notification
from mailing_service.serializers.message import MessageSerializer
from mailing_service.serializers.message_stats import serialize_stats, get_stats_dict


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def create_test_data():
    notification_data = [Notification(**{'start_datetime': '2022-09-01 10:00:00',
                                         'end_datetime': '2022-09-25 23:59:00',
                                         'text': 'Attention! Notification text!',
                                         'mailing_filter': {'tag': 'tag_1'}}),
                         Notification(**{'start_datetime': '2022-09-08 10:00:00',
                                         'end_datetime': '2022-09-20 23:59:00',
                                         'text': 'Some text for client',
                                         'mailing_filter': {'tag': 'tag_2', 'mobile_operator_code': '900'}})]
    client_data = [Client(**{'phone_number': '79007886151', 'tag': 'tag_2',
                             'mobile_operator_code': '900', 'time_zone': 'Europe/Moscow'}),
                   Client(**{'phone_number': '79220009912', 'tag': 'tag_1',
                             'mobile_operator_code': '922', 'time_zone': 'Asia/Omsk'})]
    Client.objects.bulk_create(client_data)
    Notification.objects.bulk_create(notification_data)
    msg_data = [Message(**{'notification': Notification.objects.filter(text='Attention! Notification text!').first(),
                           'client': Client.objects.filter(tag='tag_1').first(),
                           'is_sending': True}),
                Message(**{'notification': Notification.objects.filter(text='Some text for client').first(),
                           'client': Client.objects.filter(tag='tag_2').first(),
                           'is_sending': True})]
    Message.objects.bulk_create(msg_data)
    return {'notification_data': notification_data, 'client_data': client_data, 'msg_data': msg_data}


@pytest.mark.django_db
def test_message_list_by_notification_200(api_client, create_test_data):
    notification_id = create_test_data['notification_data'][0].id
    url = reverse('message-list-by-notification-view', kwargs={'pk': notification_id})
    serializer_data = MessageSerializer([create_test_data['msg_data'][0]], many=True).data
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['sent_messages'] == serializer_data


@pytest.mark.django_db
def test_message_list_by_notification_404(api_client, create_test_data):
    url = reverse('message-list-by-notification-view', kwargs={'pk': 1})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_message_stats_view(api_client, create_test_data):
    url = reverse('message-stats-view')
    queryset = Message.objects.values('notification_id', 'is_sending', 'notification__text') \
                              .annotate(count=Count('is_sending')) \
                              .values_list('notification_id', 'is_sending', 'count', 'notification__text')
    serializer_data = serialize_stats(get_stats_dict(queryset))
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer_data
