import pytest

from django.urls import reverse
from rest_framework import status

from mailing_service.models.client import Client


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def create_client_test_data():
    """
    Creating test data for testing client views
    """
    client_creating_data = [Client(**{'phone_number': '79007886151', 'tag': 'tag_1',
                                      'mobile_operator_code': '900', 'time_zone': 'Europe/Moscow'}),
                            Client(**{'phone_number': '79220009912', 'tag': 'tag_2',
                                      'mobile_operator_code': '922', 'time_zone': 'Asia/Omsk'})]
    Client.objects.bulk_create(client_creating_data)


@pytest.mark.django_db
def test_client_list_get_200(api_client, create_client_test_data):
    """
    Testing getting a list of clients (successfully)
    """
    url = reverse('client-list-view')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]['phone_number'] == '79007886151'
    assert response.data[0]['tag'] == 'tag_1'
    assert response.data[0]['mobile_operator_code'] == '900'
    assert response.data[0]['time_zone'] == 'Europe/Moscow'
    assert response.data[1]['phone_number'] == '79220009912'
    assert response.data[1]['tag'] == 'tag_2'
    assert response.data[1]['mobile_operator_code'] == '922'
    assert response.data[1]['time_zone'] == 'Asia/Omsk'


@pytest.mark.django_db
def test_client_detail_get_200(api_client, create_client_test_data):
    """
    Testing getting a client by id (successfully)
    """
    client_id = Client.objects.get(phone_number=79007886151).id
    url = reverse('client-detail-view', kwargs={'pk': client_id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['phone_number'] == '79007886151'
    assert response.data['tag'] == 'tag_1'
    assert response.data['mobile_operator_code'] == '900'
    assert response.data['time_zone'] == 'Europe/Moscow'


@pytest.mark.django_db
def test_client_detail_get_404(api_client, create_client_test_data):
    """
    Testing getting a client by id (not found, invalid id)
    """
    url = reverse('client-detail-view', kwargs={'pk': 100})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_client_post_201(api_client):
    """
    Testing creating a client (successfully)
    """
    url = reverse('client-list-view')
    creating_data = {'phone_number': '79007886151',
                     'tag': 'tag_1',
                     'mobile_operator_code': '900',
                     'time_zone': 'Asia/Yekaterinburg', }
    response = api_client.post(url, data=creating_data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
@pytest.mark.parametrize('phone_number, tag, mobile_operator_code, time_zone', [
    ('7900788615100', 'tag_1', '900', 'Asia/Omsk'),
    ('79007886151', 'tag_1', '901', 'Asia/Omsk'),
    ('79007886151', 'tag_1', '900', 'Asia/Unknown')])
def test_client_post_400(api_client, phone_number, tag, mobile_operator_code, time_zone):
    """
    Testing creating a client (bad request)
    """
    url = reverse('client-list-view')
    creating_data = {'phone_number': phone_number, 'tag': tag,
                     'mobile_operator_code': mobile_operator_code, 'time_zone': time_zone, }
    response = api_client.post(url, data=creating_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_client_put_200(api_client, create_client_test_data):
    """
    Testing updating a client (successfully)
    """
    client_id = Client.objects.get(phone_number=79220009912).id
    url = reverse('client-detail-view', kwargs={'pk': client_id})
    response = api_client.put(url, data={'tag': 'tag_new', 'time_zone': 'Europe/Moscow'})
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.parametrize('phone_number, tag, mobile_operator_code, time_zone', [
    ('7922000991200', 'tag_1', '900', 'Asia/Omsk'),
    ('79007886151', 'tag_1', '900', 'Asia/Unknown')])
def test_client_put_400(api_client, create_client_test_data, phone_number, tag, mobile_operator_code, time_zone):
    """
    Testing updating a client (successfully)
    """
    client_id = Client.objects.get(phone_number=79220009912).id
    url = reverse('client-detail-view', kwargs={'pk': client_id})
    response = api_client.put(url, data={'phone_number': phone_number, 'tag': tag,
                                         'mobile_operator_code': mobile_operator_code, 'time_zone': time_zone})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_client_put_404(api_client, create_client_test_data):
    """
    Testing updating a client (successfully)
    """
    url = reverse('client-detail-view', kwargs={'pk': 100})
    response = api_client.put(url, data={'tag': 'tag_0'})
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_client_delete_204(api_client, create_client_test_data):
    """
    Testing deleting a client (successfully)
    """
    client_id = Client.objects.get(phone_number=79220009912).id
    url = reverse('client-detail-view', kwargs={'pk': client_id})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_client_delete_404(api_client, create_client_test_data):
    """
    Testing updating a client (successfully)
    """
    url = reverse('client-detail-view', kwargs={'pk': 100})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
