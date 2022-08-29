import json
import requests

from itertools import islice
from django.db.models import Q, QuerySet
from datetime import datetime
from requests import Response
from rest_framework import status

from config.settings import OPEN_API_TOKEN
from application.entities.client import Client
from application.entities.message import Message
from application.entities.notification import Notification


def get_clients(mailing_filter: dict) -> QuerySet:
    """
    Get clients by filter
    """
    clients = Client.objects.all()
    tag = mailing_filter.get('tag')
    mobile_operator_code = mailing_filter.get('mobile_operator_code')
    if tag:
        clients = clients.filter(tag=tag)
    if mobile_operator_code:
        clients = clients.filter(mobile_operator_code=str(mobile_operator_code))

    return clients.values_list('id', 'phone_number')


def get_notifications() -> QuerySet:
    """
    Get notifications for start mailing
    """
    now = datetime.now()
    notifications = Notification.objects.filter(Q(start_datetime__lte=now) & Q(end_datetime__gte=now)).all()
    return notifications


def create_messages(messages: list):
    """
    Create message records from input data
    """
    batch_size = 100
    message_iterator = (message for message in messages)
    while True:
        batch = list(islice(message_iterator, batch_size))
        if not batch:
            break
        Message.objects.bulk_create(batch, batch_size)


def send_message(data: dict) -> Response:
    """
    Send message and return response
    """
    url = "https://probe.fbrq.cloud/v1/send/1"
    headers = {'Content-type': 'application/json', 'accept': 'application/json', 'Authorization': OPEN_API_TOKEN}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response


def start_mailing():
    """
    Start notification mailing and creating messages in database
    """
    messages = []
    for notification in get_notifications():
        reached_numbers = []
        for client_id, phone_number in get_clients(notification.mailing_filter):
            if phone_number in notification.reached_numbers:
                continue
            response = send_message(data={"id": 1, "phone": phone_number, "text": notification.text})
            mailing_status = False
            if response.status_code == status.HTTP_200_OK:
                mailing_status = True
                reached_numbers.append(phone_number)
            messages.append(Message(**{
                'notification_id': notification.id,
                'client_id': client_id,
                'is_sending': mailing_status
            }))
        if reached_numbers:
            notification.reached_numbers.extend(reached_numbers)
            notification.save()
    create_messages(messages)
