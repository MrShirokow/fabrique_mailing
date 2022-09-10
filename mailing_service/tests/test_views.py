import pytest

from django.urls import reverse
from rest_framework import status

from mailing_service.models.client import Client


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def create_test_data():
    creating_data = [Client(**{'phone_number': '79007886151', 'tag': 'tag_1',
                               'mobile_operator_code': '900', 'time_zone': 'Europe/Moscow'}),
                     Client(**{'phone_number': '79220009912', 'tag': 'tag_2',
                               'mobile_operator_code': '922', 'time_zone': 'Asia/Omsk'})]
    Client.objects.bulk_create(creating_data)


@pytest.mark.django_db
def test_client_list_get_request(api_client, create_test_data):
    url = reverse('client-list-view')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]['phone_number'] == '79007886151'
    assert response.data[0]['tag'] == 'tag_1'
    assert response.data[0]['mobile_operator_code'] == '900'
    assert response.data[0]['time_zone'] == 'Europe/Moscow'
    assert response.data[1]['phone_number'] == '79220009912'
    assert response.data[1]['tag'] == 'tag_2'
    assert response.data[1]['mobile_operator_code'] == '922'
    assert response.data[1]['time_zone'] == 'Asia/Omsk'


@pytest.mark.django_db
def test_client_detail_get_request(api_client, create_test_data):
    client_id = Client.objects.filter(phone_number=79007886151).first().id
    url = reverse('client_detail_view', kwargs={'pk': client_id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['phone_number'] == '79007886151'
    assert response.data['tag'] == 'tag_1'
    assert response.data['mobile_operator_code'] == '900'
    assert response.data['time_zone'] == 'Europe/Moscow'
