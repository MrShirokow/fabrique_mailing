import pytest

from mailing_service.models.client import Client
from mailing_service.models.message import Message
from mailing_service.models.notification import Notification


@pytest.mark.django_db
def test_client_model():
    client = Client.objects.create(
        phone_number=79007886151,
        tag='good',
        mobile_operator_code=900,
        time_zone='Asia/Omsk',
    )
    assert Client.objects.count() == 1
    assert client.phone_number == 79007886151
    assert client.tag == 'good'
    assert client.mobile_operator_code == 900
    assert client.time_zone == 'Asia/Omsk'


@pytest.mark.django_db
def test_notification_model():
    notification = Notification.objects.create(
        start_datetime='2022-09-06 10:00:00',
        end_datetime='2022-09-10 23:59:00',
        text='Attention! Notification text!',
        mailing_filter={'tag': 'tag_1', 'mobile_operator_code': 900},
    )
    assert Notification.objects.count() == 1
    assert notification.start_datetime == '2022-09-06 10:00:00'
    assert notification.end_datetime == '2022-09-10 23:59:00'
    assert notification.text == 'Attention! Notification text!'
    assert notification.mailing_filter == {'tag': 'tag_1', 'mobile_operator_code': 900}


@pytest.mark.django_db
def test_message_model():
    notification = Notification.objects.create(
        start_datetime='2022-09-06 10:00:00',
        end_datetime='2022-09-10 23:59:00',
        text='Attention! Notification text!',
        mailing_filter={'tag': 'tag_1', 'mobile_operator_code': 900},
    )
    client = Client.objects.create(
        phone_number=79007886151,
        tag='good',
        mobile_operator_code=900,
        time_zone='Asia/Omsk',
    )
    message = Message.objects.create(
        notification=notification,
        client=client,
        is_sending=True,
    )
    assert Message.objects.count() == 1
    assert message.notification == notification
    assert message.client == client
    assert message.is_sending is True
