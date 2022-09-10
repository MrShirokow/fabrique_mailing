import pytest

from django.urls import reverse
from rest_framework import status

from mailing_service.models.client import Client
from mailing_service.models.message import Message
from mailing_service.models.notification import Notification


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


@pytest.mark.django_db
def test_message_list_by_notification_200(api_client, create_test_data):
    notification_id = Notification.objects.filter(text='Attention! Notification text!').first().id
    client_id = Client.objects.filter(phone_number=79220009912).first().id
    url = reverse('message-list-by-notification-view', kwargs={'pk': notification_id})
    response = api_client.get(url)
    data = response.data['sent_messages']
    assert response.status_code == status.HTTP_200_OK
    assert data[0]['notification'] == notification_id
    assert data[0]['client'] == client_id
    assert data[0]['is_sending']


@pytest.mark.django_db
def test_message_list_by_notification_404(api_client, create_test_data):
    url = reverse('message-list-by-notification-view', kwargs={'pk': 1})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_message_stats_view(api_client, create_test_data):
    notifications = Notification.objects.all()
    url = reverse('message-stats-view')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]['notification'] == notifications.get(text='Attention! Notification text!').id
    assert response.data[0]['text'] == 'Attention! Notification text!'
    assert response.data[0]['messages'][0]['count'] == 1
    assert response.data[0]['messages'][1]['count'] == 0
    assert response.data[1]['notification'] == notifications.get(text='Some text for client').id
    assert response.data[1]['text'] == 'Some text for client'
    assert response.data[1]['messages'][0]['count'] == 1
    assert response.data[1]['messages'][1]['count'] == 0
