from django.db import connection
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response

from application.pagination import BasicPagination
from application.serializers.client_serializer import ClientListSerializer
from application.entities.client.model import Client
from application.entities.notification.model import Notification
from application.entities.message.model import Message


class ClientListAPIView(APIView, BasicPagination):
    """
    Get list of all clients or create new client
    """
    def get(self, request: Request, format=None) -> Response:
        """
        Get list of clients
        """
        clients = self.paginate_queryset(Client.objects.all(), request, view=self)
        clients_serializer = ClientListSerializer(clients, many=True)
        return Response(clients_serializer.data)

    def post(self, request: Request, format=None) -> Response:
        """
        Create a new client or 400 (bad request)
        """
        client_serializer = ClientListSerializer(data=request.data)
        if not client_serializer.is_valid():
            return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        client_serializer.save()
        return Response('client was created successfully', status=status.HTTP_201_CREATED)


class ClientAPIView(APIView):
    """
    Get, update or delete a client instance.
    """
    def get(self, request: Request, pk: int, format=None) -> Response:
        """
        Get client by id or 404
        """
        client = get_object_or_404(Client, pk=pk)
        client_serializer = ClientListSerializer(client)
        return Response(client_serializer.data)

    def put(self, request: Request, pk: int, format=None) -> Response:
        """
        Update client by id or 404
        """
        client = get_object_or_404(Client, pk=pk)
        client_serializer = ClientListSerializer(client, data=request.data)
        if not client_serializer.is_valid():
            return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        client_serializer.save()
        return Response('client was updated successfully', status=status.HTTP_200_OK)

    def delete(self, request: Request, pk: int, format=None) -> Response:
        """
        Delete client by id or 404
        """
        client = get_object_or_404(Client, pk=pk)
        client.delete()
        return Response('client was deleted successfully', status=status.HTTP_204_NO_CONTENT)


class NotificationAPIView(APIView):
    pass


class MessageAPIView(APIView):
    pass
