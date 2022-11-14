from django.contrib import admin

from mailing_service.models.client import Client
from mailing_service.models.message import Message
from mailing_service.models.notification import Notification
from mailing_service.models.success_client import SuccessClient


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_datetime', 'end_datetime', 'text', 'mailing_filter')
    list_display_links = ('id', 'text')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'mobile_operator_code', 'tag', 'time_zone')
    list_display_links = ('id', 'phone_number')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'notification', 'client', 'created_at', 'is_sending')
    list_display_links = ('id', )


@admin.register(SuccessClient)
class SuccessClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'notification', 'client')
    list_display_links = list_display
