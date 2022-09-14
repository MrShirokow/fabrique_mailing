import pytest
import datetime

from mailing_service import mailing
from mailing_service.models.message import Message
from mailing_service.models.client import Client
from mailing_service.models.notification import Notification


@pytest.fixture
def create_test_data():
    start_datetime = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    end_datetime = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    notification_data = [Notification(**{'start_datetime': f'{start_datetime} 10:00:00',
                                         'end_datetime': f'{end_datetime} 23:59:59',
                                         'text': 'First Notification',
                                         'mailing_filter': {'tag': 'tag_1'}}),
                         Notification(**{'start_datetime': f'{start_datetime} 10:00:00',
                                         'end_datetime': f'{end_datetime} 23:59:59',
                                         'text': 'Second Notification',
                                         'mailing_filter': {'tag': 'tag_1', 'mobile_operator_code': '922'}}),
                         Notification(**{'start_datetime': '2020-10-10 10:00:00',
                                         'end_datetime': '2020-10-20 23:59:59',
                                         'text': 'It was sent',
                                         'mailing_filter': {'mobile_operator_code': '900'}})]
    client_data = [Client(**{'phone_number': '79227886151', 'tag': 'tag_1',
                             'mobile_operator_code': '922', 'time_zone': 'Europe/Moscow'}),
                   Client(**{'phone_number': '79220009912', 'tag': 'tag_2',
                             'mobile_operator_code': '922', 'time_zone': 'Asia/Omsk'}),
                   Client(**{'phone_number': '79001459134', 'tag': 'tag_1',
                             'mobile_operator_code': '900', 'time_zone': 'Asia/Omsk'})]
    Client.objects.bulk_create(client_data)
    Notification.objects.bulk_create(notification_data)
    return {'notification_data': notification_data, 'client_data': client_data}


@pytest.mark.django_db
def test_mailing_get_notification(create_test_data):
    notifications = mailing.get_notifications()
    assert list(notifications) == create_test_data['notification_data'][:2]


@pytest.mark.django_db
def test_mailing_get_clients(create_test_data):
    clients = mailing.get_clients({'tag': 'tag_1', 'mobile_operator_code': '922'})
    expected_client = create_test_data['client_data'][0]
    assert list(clients) == [(expected_client.id, expected_client.phone_number)]


@pytest.mark.django_db
def test_mailing_create_messages(create_test_data):
    messages = [Message(**{'notification': create_test_data['notification_data'][0],
                           'client': create_test_data['client_data'][1],
                           'is_sending': True}),
                Message(**{'notification': create_test_data['notification_data'][1],
                           'client': create_test_data['client_data'][0],
                           'is_sending': True})]
    mailing.create_messages(messages)
    assert Message.objects.count() == 2
    assert Message.objects.get(pk=messages[0].id)
    assert Message.objects.get(pk=messages[1].id)


def test_mailing_send_message():
    response_ok = mailing.send_message(data={'id': 1, 'phone': 79635709980, 'text': 'Some Text'})
    response_bad = mailing.send_message(data={'id': 2, 'phone': 79635709980, 'text': 'Some Text'})
    assert response_ok.status_code == 200
    assert response_bad.status_code == 400


@pytest.mark.django_db
def test_start_mailing(create_test_data):
    assert Message.objects.count() == 0
    mailing.start()
    assert Message.objects.count() == 3
