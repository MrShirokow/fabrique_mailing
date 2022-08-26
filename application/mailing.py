import json
import requests

from django.db.models import Q, QuerySet
from datetime import datetime
from requests import Response
from rest_framework import status

from config.settings import OPEN_API_TOKEN
from application.entities.client import Client
from application.entities.notification import Notification
from application.serializers.message import MessageSerializer


def send_message(data: dict) -> Response:
    """
    Send message and return response
    """
    url = "https://probe.fbrq.cloud/v1/send/1"
    headers = {'Content-type': 'application/json', 'accept': 'application/json', 'Authorization': OPEN_API_TOKEN}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response


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
    notifications = Notification.objects.filter(Q(start_datetime__lte=now) & Q(end_datetime__gte=now))\
                                        .values_list('id', 'text', 'mailing_filter')
    return notifications


def create_message(data):
    message_serializer = MessageSerializer(data=data)
    if message_serializer.is_valid():
        message_serializer.save()


def start_mailing():
    notifications = get_notifications()
    for notification_id, text, mailing_filter in notifications:
        clients = get_clients(mailing_filter)
        for client_id, phone_number in clients:
            response = send_message(data={"id": 1, "phone": phone_number, "text": text})
            mailing_status = False
            if response.status_code == status.HTTP_200_OK:
                mailing_status = True
            data = {
                'notification': notification_id,
                'client': client_id,
                'is_sending': mailing_status
            }
            create_message(data)
