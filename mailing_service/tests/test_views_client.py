import pytest

from django.urls import reverse
from rest_framework import status

from mailing_service.models.client import Client
from mailing_service.serializers.client import ClientSerializer


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def client_test_data():
    creating_data = [Client(**{'phone_number': '79007886151', 'tag': 'tag_1',
                               'mobile_operator_code': '900', 'time_zone': 'Europe/Moscow'}),
                     Client(**{'phone_number': '79220009912', 'tag': 'tag_2',
                               'mobile_operator_code': '922', 'time_zone': 'Asia/Omsk'})]
    Client.objects.bulk_create(creating_data)
    return creating_data


@pytest.mark.django_db
def test_client_list_get_200(api_client, client_test_data):
    url = reverse('client-list-view')
    serializer_data = ClientSerializer(client_test_data, many=True).data
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer_data


@pytest.mark.django_db
def test_client_detail_get_200(api_client, client_test_data):
    client = client_test_data[0]
    url = reverse('client-detail-view', kwargs={'pk': client.id})
    serializer_data = ClientSerializer(client).data
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer_data


@pytest.mark.django_db
def test_client_detail_get_404(api_client, client_test_data):
    url = reverse('client-detail-view', kwargs={'pk': 1})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_client_post_201(api_client):
    url = reverse('client-list-view')
    creating_data = {'phone_number': '79007886151',
                     'tag': 'tag_1',
                     'mobile_operator_code': '900',
                     'time_zone': 'Asia/Yekaterinburg', }
    response = api_client.post(url, data=creating_data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
@pytest.mark.parametrize('data', [
    ({'tag': 'tag_new', 'time_zone': 'Europe/Moscow'}),
    ({'phone_number': '79017886151', 'mobile_operator_code': '901'}),
    ({'phone_number': '7900788615100', 'tag': 'tag_1', 'mobile_operator_code': '900', 'time_zone': 'Asia/Omsk'}),
    ({'phone_number': '79007886151', 'tag': 'tag_1', 'mobile_operator_code': '901', 'time_zone': 'Asia/Omsk'}),
    ({'phone_number': '79017886151', 'tag': 'tag_1', 'mobile_operator_code': '901', 'time_zone': 'Asia/Unknown'})])
def test_client_post_400(api_client, data):
    url = reverse('client-list-view')
    response = api_client.post(url, data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.parametrize('data', [
    ({'tag': 'tag_new', 'time_zone': 'Europe/Moscow'}),
    ({'phone_number': '79017886151', 'tag': 'tag_1', 'mobile_operator_code': '901', 'time_zone': 'Asia/Omsk'}),
    ({'phone_number': '79017886151', 'mobile_operator_code': '901'}),
    ({'time_zone': 'Asia/Yekaterinburg'})])
def test_client_put_200(api_client, client_test_data, data):
    client_id = client_test_data[0].id
    url = reverse('client-detail-view', kwargs={'pk': client_id})
    response = api_client.put(url, data=data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.parametrize('data', [
    ({'tag': 'tag_new', 'time_zone': 'Europe/NewCity'}),
    ({'phone_number': '7901788615100', 'tag': 'tag_1', 'mobile_operator_code': '901', 'time_zone': 'Asia/Omsk'}),
    ({'phone_number': '79017886151', 'mobile_operator_code': '911'}),
    ({'phone_number': '79881003340'}),
    ({'mobile_operator_code': '933'})])
def test_client_put_400(api_client, client_test_data, data):
    client_id = client_test_data[0].id
    url = reverse('client-detail-view', kwargs={'pk': client_id})
    response = api_client.put(url, data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_client_put_404(api_client, client_test_data):
    url = reverse('client-detail-view', kwargs={'pk': 1})
    response = api_client.put(url, data={'tag': 'tag_0'})
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_client_delete_204(api_client, client_test_data):
    client_id = client_test_data[0].id
    url = reverse('client-detail-view', kwargs={'pk': client_id})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_client_delete_404(api_client, client_test_data):
    url = reverse('client-detail-view', kwargs={'pk': 1})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
