import json
import requests
import logging

from itertools import islice
from celery import shared_task
from celery.result import allow_join_result
from datetime import datetime
from rest_framework import status
from django.apps import apps
from django.db.models import Q, QuerySet

import mailing_service.logging.log_messages_creator as log

from mailing_service.models.client import Client
from mailing_service.models.notification import Notification
from mailing_service.models.success_client import SuccessClient
from config.settings import OPEN_API_TOKEN, MAILING_SERVICE_URL, ACCEPT, CONTENT_TYPE


def get_notifications() -> QuerySet:
    """
    Get notifications for start mailing
    """
    now = datetime.now()
    notifications = Notification.objects.filter(
        Q(start_datetime__lte=now) & Q(end_datetime__gte=now)
    ).values('id', 'text', 'mailing_filter')
    return notifications


def get_clients(mailing_filter: dict, notification_id: int) -> QuerySet:
    """
    Get clients for mailing by filter
    """
    tag = mailing_filter.get('tag')
    mobile_operator_code = mailing_filter.get('mobile_operator_code')
    query = SuccessClient.objects.filter(
        notification_id=notification_id
    ).values('client_id')
    success_ids = {client['client_id'] for client in query}

    clients = Client.objects.all()
    if tag:
        clients = clients.filter(tag=tag)
    if mobile_operator_code:
        clients = clients.filter(mobile_operator_code=str(mobile_operator_code))
    clients = clients.exclude(
        id__in=success_ids
    ).values_list('id', 'phone_number')
    return clients


@shared_task(ignore_result=True)
def create_model_entries(model_name: str, data: list):
    """
    Create model entries from list data
    """
    model = apps.get_model('mailing_service', model_name)
    batch_size = 100
    obj_iterator = (model(**obj) for obj in data)
    while True:
        batch = list(islice(obj_iterator, batch_size))
        if not batch:
            break
        model.objects.bulk_create(batch, batch_size)


@shared_task
def send_message(data: dict) -> tuple[int, datetime]:
    """
    Send message and return response status and sending time
    """
    headers = {'Content-type': CONTENT_TYPE, 'accept': ACCEPT, 'Authorization': OPEN_API_TOKEN}
    response = requests.post(MAILING_SERVICE_URL, data=json.dumps(data), headers=headers)
    now = datetime.now()
    logging.info(log.create_mailing_log_message(response.request, response))
    return response.status_code, now


@shared_task(ignore_result=True)
def run_mailing():
    """
    Start notification mailing and creating messages in database
    """
    messages_data = []
    success_clients_data = []
    for notification in get_notifications():
        for client_id, phone_number in get_clients(notification['mailing_filter'], notification['id']):
            with allow_join_result():
                result = send_message.delay({
                    "id": 1, 
                    "phone": phone_number, 
                    "text": notification['text'],
                }).get()

            mailing_status = False
            if result[0] == status.HTTP_200_OK:
                mailing_status = True
                success_clients_data.append({
                    'notification_id_id': notification['id'],
                    'client_id_id': client_id,
                })
            messages_data.append({
                'notification_id': notification['id'],
                'client_id': client_id,
                'is_sending': mailing_status,
                'created_at': result[1],
            })
    create_model_entries.delay('SuccessClient', success_clients_data)
    create_model_entries.delay('Message', messages_data)
