import pytest
import datetime

from mailing_service import tasks
from mailing_service.models.message import Message
from mailing_service.models.client import Client
from mailing_service.models.notification import Notification
from mailing_service.models.success_client import SuccessClient


@pytest.fixture
def mailing_test_data():
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
def test_mailing_get_notification(mailing_test_data):
    notifications = tasks.get_notifications()
    expected = [{
        'id': notification.id, 
        'text': notification.text, 
        'mailing_filter': notification.mailing_filter
    } for notification in mailing_test_data['notification_data'][:2]]
    assert list(notifications) == expected


@pytest.mark.django_db
def test_mailing_get_clients(mailing_test_data):
    notification = mailing_test_data['notification_data'][1]
    clients = tasks.get_clients(notification.mailing_filter, notification.id)
    expected_client = mailing_test_data['client_data'][0]
    assert list(clients) == [(expected_client.id, expected_client.phone_number)]


@pytest.mark.django_db
@pytest.mark.parametrize('model_name', ['Message', 'SuccessClient'])
def test_mailing_create_model_entries(mailing_test_data, model_name):
    message_data = [
        {
            'notification': mailing_test_data['notification_data'][0],
            'client': mailing_test_data['client_data'][1],
            'is_sending': True
        },
        {
            'notification': mailing_test_data['notification_data'][1],
            'client': mailing_test_data['client_data'][0],
            'is_sending': True
        }
    ]
    success_clients_data = [
        {
            'notification_id': mailing_test_data['notification_data'][0].id,
            'client_id': mailing_test_data['client_data'][1].id,
        },
        {
            'notification_id': mailing_test_data['notification_data'][1].id,
            'client_id': mailing_test_data['client_data'][0].id,
        }
    ]
    data = {'Message': message_data, 'SuccessClient': success_clients_data}
    models = {'Message': Message, 'SuccessClient': SuccessClient}
    assert models[model_name].objects.count() == 0
    tasks.create_model_entries(model_name, data[model_name])
    assert models[model_name].objects.count() == 2


def test_mailing_send_message():
    status_ok, time = tasks.send_message(data={'id': 1, 'phone': 79635709980, 'text': 'Some Text'})
    status_bad, time = tasks.send_message(data={'id': 2, 'phone': 79635709980, 'text': 'Some Text'})
    assert status_ok == 200
    assert status_bad == 400


# @pytest.mark.django_db
# def test_run_mailing(mailing_test_data):
#     assert Message.objects.count() == 0
#     tasks.run_mailing()
#     assert Message.objects.count() == 3
