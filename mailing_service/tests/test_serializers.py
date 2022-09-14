import pytest

from collections import defaultdict
from django.db.models import Count

import mailing_service.serializers.message_stats as message_stats

from mailing_service.models.message import Message
from mailing_service.serializers.client import ClientSerializer
from mailing_service.serializers.message import MessageSerializer
from mailing_service.serializers.notification import NotificationSerializer
from mailing_service.tests.test_views_message_stats import create_test_data


@pytest.fixture
def data_for_message_stats():
    return Message.objects.values('notification_id', 'is_sending', 'notification__text') \
        .annotate(count=Count('is_sending')) \
        .values_list('notification_id', 'is_sending', 'count', 'notification__text')


@pytest.mark.django_db
def test_client_serializer(create_test_data):
    data = ClientSerializer(create_test_data['client_data'], many=True).data
    expected_data = [
        {
            'id': create_test_data['client_data'][0].id,
            'phone_number': '79007886151',
            'tag': 'tag_2',
            'mobile_operator_code': '900',
            'time_zone': 'Europe/Moscow'
        },
        {
            'id': create_test_data['client_data'][1].id,
            'phone_number': '79220009912',
            'tag': 'tag_1',
            'mobile_operator_code': '922',
            'time_zone': 'Asia/Omsk'
        }
    ]
    assert data == expected_data


@pytest.mark.django_db
def test_notification_serializer(create_test_data):
    data = NotificationSerializer(create_test_data['notification_data'], many=True).data
    expected_data = [
        {
            'id': create_test_data['notification_data'][0].id,
            'start_datetime': '2022-09-01 10:00:00',
            'end_datetime': '2022-09-25 23:59:00',
            'text': 'Attention! Notification text!',
            'mailing_filter': {'tag': 'tag_1'}
        },
        {
            'id': create_test_data['notification_data'][1].id,
            'start_datetime': '2022-09-08 10:00:00',
            'end_datetime': '2022-09-20 23:59:00',
            'text': 'Some text for client',
            'mailing_filter': {'tag': 'tag_2', 'mobile_operator_code': '900'}
        }
    ]
    assert data == expected_data


@pytest.mark.django_db
def test_message_serializer(create_test_data):
    data = MessageSerializer(create_test_data['msg_data'], many=True).data
    expected_data = [
        {
            'id': create_test_data['msg_data'][0].id,
            'notification': create_test_data['notification_data'][0].id,
            'client': create_test_data['client_data'][1].id,
            'is_sending': True
        },
        {
            'id': create_test_data['msg_data'][1].id,
            'notification': create_test_data['notification_data'][1].id,
            'client': create_test_data['client_data'][0].id,
            'is_sending': True
        }
    ]
    assert data == expected_data


@pytest.mark.django_db
def test_get_stats_dict(create_test_data, data_for_message_stats):
    data = message_stats.get_stats_dict(data_for_message_stats)
    expected_data = defaultdict(lambda: defaultdict(int), [
        (create_test_data['notification_data'][0].id, defaultdict(int, {
            True: 1,
            'text': 'Attention! Notification text!'
        })),
        (create_test_data['notification_data'][1].id, defaultdict(int, {
            True: 1,
            'text': 'Some text for client'
        }))
    ])
    assert data == expected_data


@pytest.mark.django_db
def test_message_stats_serializer(create_test_data, data_for_message_stats):
    data = message_stats.serialize_stats(message_stats.get_stats_dict(data_for_message_stats))
    expected_data = [
        {
            'notification': create_test_data['notification_data'][0].id,
            'text': 'Attention! Notification text!',
            'messages': [
                {
                    'is_sending': True,
                    'count': 1
                },
                {
                    'is_sending': False,
                    'count': 0
                }
            ]
        },
        {
            'notification': create_test_data['notification_data'][1].id,
            'text': 'Some text for client',
            'messages': [
                {
                    'is_sending': True,
                    'count': 1
                },
                {
                    'is_sending': False,
                    'count': 0
                }
            ]
        }
    ]
    assert sorted(data, key=lambda d: d['notification']) == expected_data
