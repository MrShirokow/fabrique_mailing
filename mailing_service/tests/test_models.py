import pytest

from django.db import DataError, IntegrityError
from django.core.exceptions import ValidationError

from mailing_service.models.client import Client
from mailing_service.models.message import Message
from mailing_service.models.notification import Notification


@pytest.mark.django_db
def test_client_model_ok():
    """
    Testing successful creating of  client model
    """
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
def test_client_unique_phone_number():
    """
    Testing unique of phone number
    """
    Client.objects.create(phone_number='79007886151', tag='tag_1',
                          mobile_operator_code='900', time_zone='Asia/Yekaterinburg')
    with pytest.raises(IntegrityError):
        Client.objects.create(phone_number='79007886151', tag='tag_2',
                              mobile_operator_code='900', time_zone='Europe/Moscow')


@pytest.mark.django_db
@pytest.mark.parametrize('error, phone_number, tag, mobile_operator_code, time_zone', [
    (ValidationError, '79001005070', 'tag_1', '900', 'Europe/Unknown'),
    (DataError, '79001005070', 'tag_1', '9111', 'Europe/Moscow'),
    (DataError, '7900100507080', 'tag_1', '900', 'Europe/Moscow')])
def test_client_model_with_error(error, phone_number, tag, mobile_operator_code, time_zone):
    """
    Testing creating client model with error
    """
    with pytest.raises(error):
        Client.objects.create(
            phone_number=phone_number,
            tag=tag,
            mobile_operator_code=mobile_operator_code,
            time_zone=time_zone,
        )


@pytest.mark.django_db
def test_notification_model():
    """
    Testing successful creating of notification model
    """
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
@pytest.mark.parametrize('error, start_datetime, end_datetime, text, mailing_filter', [
    (ValidationError, '2022-09-32 10:00:00', '2022-09-10 10:00:00', 'Some text', {'mobile_operator_code': 900}),
    (ValidationError, '2022-09-10 10:00:00', '2022-09-32 10:00:00', 'Some text', {'tag': 'tag_1'}),
    (IntegrityError, '2022-09-10 10:00:00', '2022-09-11 10:00:00', 'Some text', None),
    (IntegrityError, '2022-09-10 10:00:00', '2022-09-11 10:00:00', None, {'tag': 'tag_1'})])
def test_notification_model_with_error(error, start_datetime, end_datetime, text, mailing_filter):
    """
    Testing creating notification model with error
    """
    with pytest.raises(error):
        Notification.objects.create(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            text=text,
            mailing_filter=mailing_filter,
        )


@pytest.mark.django_db
def test_message_model():
    """
    Testing successful creating of message model
    """
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
