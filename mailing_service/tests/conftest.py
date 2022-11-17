import datetime
import pytest

from django.conf import settings

from mailing_service.models.client import Client
from mailing_service.models.message import Message
from mailing_service.models.notification import Notification


def pytest_configure():
    """Set up Django settings for tests.

    `pytest` automatically calls this function once when tests are run.
    """
    settings.DATABASES['default']['HOST'] = 'localhost'
    settings.DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
    settings.DATABASES['default']['NAME'] = 'postgres'
    settings.DATABASES['default']['USER'] = 'postgres'
    settings.DATABASES['default']['PASSWORD'] = 'postgres'
    settings.DATABASES['default']['PORT'] = '5432'
    settings.CELERY_TASK_ALWAYS_EAGER = True


@pytest.fixture(scope="session", autouse=True)
def django_db_setup(django_db_setup):
    """Set up test db for testing"""


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(django_db_setup, db):
    """This hook allows all tests to access DB"""


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def notification_test_data():
    creating_data = [
        Notification(
            start_datetime='2022-09-01T10:00:00',
            end_datetime='2022-09-25T23:59:00',
            text='Attention! Notification text!',
            mailing_filter={'tag': 'tag_1'}
        ),
        Notification(
            start_datetime='2022-09-08T10:00:00',
            end_datetime='2022-09-20T23:59:00',
            text='Some text for client',
            mailing_filter={'tag': 'tag_2', 'mobile_operator_code': '900'}
        )
    ]
    Notification.objects.bulk_create(creating_data)
    return creating_data


@pytest.fixture
def client_test_data():
    creating_data = [
        Client(
            phone_number='79007886151', 
            tag='tag_1',
            mobile_operator_code='900', 
            time_zone='Europe/Moscow'
        ),
        Client(
            phone_number='79220009912', 
            tag='tag_2',
            mobile_operator_code='922', 
            time_zone='Asia/Omsk'
    )]
    Client.objects.bulk_create(creating_data)
    return creating_data


@pytest.fixture
def general_test_data():
    notification_data = [
        Notification(
            start_datetime='2022-09-01 10:00:00',
            end_datetime='2022-09-25 23:59:00',
            text='Attention! Notification text!',
            mailing_filter={'tag': 'tag_1'}
        ),
        Notification(
            start_datetime='2022-09-08 10:00:00',
            end_datetime='2022-09-20 23:59:00',
            text='Some text for client',
            mailing_filter={'tag': 'tag_2', 'mobile_operator_code': '900'}
        )
    ]
    client_data = [
        Client(
            phone_number='79007886151', 
            tag='tag_2',
            mobile_operator_code='900', 
            time_zone='Europe/Moscow'
        ),
        Client(
            phone_number='79220009912', 
            tag='tag_1',
            mobile_operator_code='922', 
            time_zone='Asia/Omsk'
        )
    ]
    Client.objects.bulk_create(client_data)
    Notification.objects.bulk_create(notification_data)
    msg_data = [
        Message(
            notification_id=notification_data[0].id,
            client_id=client_data[1].id,
            is_sending=True
        ),
        Message(
            notification_id=notification_data[1].id,
            client_id=client_data[0].id,
            is_sending=True
    )]
    Message.objects.bulk_create(msg_data)
    return {
        'notification_data': notification_data, 
        'client_data': client_data, 
        'msg_data': msg_data
    }


@pytest.fixture
def mailing_test_data():
    start_datetime = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    end_datetime = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    notification_data = [
        Notification(
            start_datetime=f'{start_datetime} 10:00:00',
            end_datetime=f'{end_datetime} 23:59:59',
            text='First Notification',
            mailing_filter={'tag': 'tag_1'}
        ),
        Notification(
            start_datetime=f'{start_datetime} 10:00:00',
            end_datetime=f'{end_datetime} 23:59:59',
            text='Second Notification',
            mailing_filter={'tag': 'tag_1', 'mobile_operator_code': '922'}
        ),
        Notification(
            start_datetime='2020-10-10 10:00:00',
            end_datetime='2020-10-20 23:59:59',
            text='It was sent',
            mailing_filter={'mobile_operator_code': '900'}
        )
    ]
    client_data = [
        Client(
            phone_number='79227886151', 
            tag='tag_1',
            mobile_operator_code='922', 
            time_zone='Europe/Moscow'
        ),
        Client(
            phone_number='79220009912', 
            tag='tag_2',
            mobile_operator_code='922', 
            time_zone='Asia/Omsk'
        ),
        Client(
            phone_number='79001459134', 
            tag='tag_1',
            mobile_operator_code='900', 
            time_zone='Asia/Omsk'
        )
    ]
    Client.objects.bulk_create(client_data)
    Notification.objects.bulk_create(notification_data)
    return {'notification_data': notification_data, 'client_data': client_data}
