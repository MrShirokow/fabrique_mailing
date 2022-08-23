import json

from django.db import connection
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpRequest, JsonResponse, HttpResponseNotFound, HttpResponse

from application.serializers.client_serializer import ClientListSerializer
from application.entities.client.model import Client
from application.entities.notification.model import Notification
from application.entities.message.model import Message
from application.entities.client.form import ClientForm
from application.entities.notification.form import NotificationForm
from application.entities.message.form import MessageForm


class ClientListAPIView(APIView):
    def get(self, request: Request) -> Response:
        clients = ClientListSerializer(instance=Client.objects.all(), many=True)
        return Response(clients.data)

    def post(self, request: Request) -> Response:
        client_serializer = ClientListSerializer(data=request.data)
        if not client_serializer.is_valid():
            return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        client_serializer.save()
        return Response('client was created successfully', status=status.HTTP_201_CREATED)


class ClientAPIView(APIView):
    def get(self, request: Request) -> Response:
        clients = ClientListSerializer(instance=Client.objects.all(), many=True)
        return Response(clients.data)

    def post(self, request: Request) -> Response:
        client_serializer = ClientListSerializer(data=request.data)
        if not client_serializer.is_valid():
            return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        client_serializer.save()
        return Response('client was created successfully', status=status.HTTP_201_CREATED)

    def put(self, request: Request) -> Response:
        client_serializer = ClientListSerializer(data=request.data)
        if not client_serializer.is_valid():
            return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response('client was updated successfully', status=200)

    def delete(self, request: Request) -> Response:
        return Response('client was deleted successfully', status=200)


class NotificationAPIView(APIView):
    pass


class MessageAPIView(APIView):
    pass
