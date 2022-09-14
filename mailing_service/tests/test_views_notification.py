import pytest

from django.urls import reverse
from rest_framework import status

from mailing_service.models.notification import Notification


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def create_notification_test_data():
    creating_data = [Notification(**{'start_datetime': '2022-09-01 10:00:00',
                                     'end_datetime': '2022-09-25 23:59:00',
                                     'text': 'Attention! Notification text!',
                                     'mailing_filter': {'tag': 'tag_1'}}),
                     Notification(**{'start_datetime': '2022-09-08 10:00:00',
                                     'end_datetime': '2022-09-20 23:59:00',
                                     'text': 'Some text for client',
                                     'mailing_filter': {'tag': 'tag_2', 'mobile_operator_code': '900'}})]
    Notification.objects.bulk_create(creating_data)


@pytest.mark.django_db
def test_notification_list_get_200(api_client, create_notification_test_data):
    url = reverse('notification-list-view')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]['start_datetime'] == '2022-09-01T10:00:00'
    assert response.data[0]['end_datetime'] == '2022-09-25T23:59:00'
    assert response.data[0]['text'] == 'Attention! Notification text!'
    assert response.data[0]['mailing_filter'] == {'tag': 'tag_1'}
    assert response.data[1]['start_datetime'] == '2022-09-08T10:00:00'
    assert response.data[1]['end_datetime'] == '2022-09-20T23:59:00'
    assert response.data[1]['text'] == 'Some text for client'
    assert response.data[1]['mailing_filter'] == {'tag': 'tag_2', 'mobile_operator_code': '900'}


@pytest.mark.django_db
def test_notification_detail_get_200(api_client, create_notification_test_data):
    notification_id = Notification.objects.filter(text='Attention! Notification text!').first().id
    url = reverse('notification-detail-view', kwargs={'pk': notification_id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['start_datetime'] == '2022-09-01T10:00:00'
    assert response.data['end_datetime'] == '2022-09-25T23:59:00'
    assert response.data['text'] == 'Attention! Notification text!'
    assert response.data['mailing_filter'] == {'tag': 'tag_1'}


@pytest.mark.django_db
def test_notification_detail_get_404(api_client, create_notification_test_data):
    url = reverse('notification-detail-view', kwargs={'pk': 1})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_notification_post_201(api_client):
    url = reverse('notification-list-view')
    creating_data = {'start_datetime': '2022-09-01 10:00:00',
                     'end_datetime': '2022-09-15 10:00:00',
                     'text': 'Hello!',
                     'mailing_filter': {'tag': 'tag_1', 'mobile_operator_code': '900'}}
    response = api_client.post(url, data=creating_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
@pytest.mark.parametrize('data', [
    ({'start_datetime': '2022-09-10 10:00:00', 'end_datetime': '2022-09-20 23:59:00'}),
    ({'text': 'Some text for client', 'mailing_filter': {'tag': 'tag_1'}}),
    ({'start_datetime': '2022-09-32 10:00:00', 'end_datetime': '2022-09-20 23:59:00',
      'text': 'Some text for client', 'mailing_filter': {'tag': 'tag_1'}}),
    ({'start_datetime': '2022-09-01 10:00:00', 'end_datetime': '2022-09-20 23:59:00',
      'text': 'Text', 'mailing_filter': {'what': 'is this'}}),
    ({'start_datetime': '2022-09-01 10:00:00', 'end_datetime': '2022-09-20 23:59:00',
      'text': 'Text', 'mailing_filter': 'filter'})])
def test_notification_post_400(api_client, data):
    url = reverse('notification-list-view')
    response = api_client.post(url, data=data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.parametrize('data', [
    ({'start_datetime': '2022-09-03 10:00:00', 'end_datetime': '2022-09-20 23:59:00',
      'text': 'Some text for client', 'mailing_filter': {'tag': 'tag_2', 'mobile_operator_code': '922'}}),
    ({'start_datetime': '2022-09-10 10:00:00', 'end_datetime': '2022-09-29 23:59:00'}),
    ({'mailing_filter': {'tag': 'tag_new'}}),
    ({'text': 'New text!!!'})])
def test_notification_put_200(api_client, create_notification_test_data, data):
    notification_id = Notification.objects.filter(text='Attention! Notification text!').first().id
    url = reverse('notification-detail-view', kwargs={'pk': notification_id})
    response = api_client.put(url, data=data, format='json')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.parametrize('data', [
    ({'start_datetime': '2022-09-10 10:00:00', 'end_datetime': '2022-09-32 23:59:00'}),
    ({'text': 'Some text for client', 'mailing_filter': {'unknown': 'attr'}}),
    ({'mailing_filter': 'filter'}),
    ({'start_datetime': '2022-09-32 10:00:00', 'end_datetime': '2022-09-20 23:59:00',
      'text': 'Some text for client', 'mailing_filter': {'tag': 'tag_1'}})])
def test_notification_put_400(api_client, create_notification_test_data, data):
    notification_id = Notification.objects.filter(text='Some text for client').first().id
    url = reverse('notification-detail-view', kwargs={'pk': notification_id})
    response = api_client.put(url, data=data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_notification_put_404(api_client, create_notification_test_data):
    url = reverse('notification-detail-view', kwargs={'pk': 1})
    response = api_client.put(url, data={'text': 'New text'})
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_notification_delete_204(api_client, create_notification_test_data):
    notification_id = Notification.objects.filter(text='Attention! Notification text!').first().id
    url = reverse('notification-detail-view', kwargs={'pk': notification_id})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_notification_delete_404(api_client, create_notification_test_data):
    url = reverse('notification-detail-view', kwargs={'pk': 1})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
