import pytest
import datetime

from unittest import mock

from mailing_service import tasks
from mailing_service.models.message import Message
from mailing_service.models.success_client import SuccessClient
from mailing_service.tasks import create_model_entries


def test_mailing_get_notification(mailing_test_data):
    notifications = tasks.get_notifications()
    expected = [
        {
            'id': notification.id, 
            'text': notification.text, 
            'mailing_filter': notification.mailing_filter
        } 
        for notification in mailing_test_data['notification_data'][:2]
    ]
    assert list(notifications) == expected


def test_mailing_get_clients(mailing_test_data):
    notification = mailing_test_data['notification_data'][1]
    clients = tasks.get_clients(notification.mailing_filter, notification.id)
    expected_client = mailing_test_data['client_data'][0]
    assert list(clients) == [(expected_client.id, expected_client.phone_number)]


@pytest.mark.celery
def test_mailing_send_message(celery_worker):
    status_ok, _ = tasks.send_message.delay({
        'id': 1, 'phone': 79635709980, 'text': 'Some Text'
    }).get()
    status_bad, _ = tasks.send_message.delay({
        'id': 2, 'phone': 79635709980, 'text': 'Some Text'
    }).get()
    assert status_ok == 200
    assert status_bad == 400


@pytest.mark.django_db(transaction=True)
@pytest.mark.celery
@pytest.mark.parametrize('model_name', ['Message', 'SuccessClient'])
def test_mailing_create_model_entries(mailing_test_data, celery_worker, model_name):
    message_data = [
        {
            'notification_id': mailing_test_data['notification_data'][0].id,
            'client_id': mailing_test_data['client_data'][1].id,
            'is_sending': True
        },
        {
            'notification_id': mailing_test_data['notification_data'][1].id,
            'client_id': mailing_test_data['client_data'][0].id,
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
    task_result = tasks.create_model_entries.delay(model_name, data[model_name])
    _ = task_result.get()
    assert task_result.status == 'SUCCESS'
    assert models[model_name].objects.count() == 2


@mock.patch('celery.result.AsyncResult.get', lambda data: (200, datetime.datetime.now()))
@mock.patch('mailing_service.tasks.create_model_entries', create_model_entries)
def test_run_mailing(mailing_test_data):
    assert Message.objects.count() == 0
    assert SuccessClient.objects.count() == 0
    tasks.run_mailing()
    assert SuccessClient.objects.count() == 3
    assert Message.objects.count() == 3
