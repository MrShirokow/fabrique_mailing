import pytest

from django.db import DataError
from django.core.exceptions import ValidationError

from mailing_service.models.client import Client
from mailing_service.models.message import Message
from mailing_service.models.notification import Notification


@pytest.mark.django_db
def test_client_model():
    client = Client.objects.create(
        phone_number='79007886151',
        tag='tag_1',
        mobile_operator_code='900',
        time_zone='Asia/Yekaterinburg',
    )
    assert Client.objects.count() == 1
    assert client.phone_number == '79007886151'
    assert client.tag == 'tag_1'
    assert client.mobile_operator_code == '900'
    assert client.time_zone == 'Asia/Yekaterinburg'
    assert client.__str__() == '79007886151'


@pytest.mark.django_db
@pytest.mark.parametrize('error, phone_number, tag, mobile_operator_code, time_zone', [
    (ValidationError, '79001005070', 'tag_1', '900', 'Europe/Unknown'),
    (DataError, '79001005070', 'tag_1', '9111', 'Europe/Moscow'),
    (DataError, '7900100507080', 'tag_1', '900', 'Europe/Moscow')])
def test_client_model_with_error(error, phone_number, tag, mobile_operator_code, time_zone):
    with pytest.raises(error):
        Client.objects.create(
            phone_number=phone_number,
            tag=tag,
            mobile_operator_code=mobile_operator_code,
            time_zone=time_zone,
        )


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
    assert notification.__str__() == f'notification #{notification.id}'


@pytest.mark.django_db
def test_message_model():
    notification = Notification.objects.create(start_datetime='2022-09-06 10:00:00',
                                               end_datetime='2022-09-10 23:59:00',
                                               text='Attention! Notification text!',
                                               mailing_filter={'tag': 'tag_1', 'mobile_operator_code': 900})
    client = Client.objects.create(phone_number=79007886151,
                                   tag='tag_1',
                                   mobile_operator_code=900,
                                   time_zone='Asia/Omsk')
    message = Message.objects.create(notification=notification,
                                     client=client,
                                     is_sending=True)
    assert Message.objects.count() == 1
    assert message.notification == notification
    assert message.client == client
    assert message.is_sending is True
    assert message.__str__() == f'message #{message.id}'
