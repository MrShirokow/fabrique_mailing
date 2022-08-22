from django.contrib import admin

from application.app_models.client import Client
from application.app_models.message import Message
from application.app_models.notification import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_datetime', 'end_datetime')
    list_display_links = ('id', )


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'mobile_operator_code', 'tag', 'time_zone')
    list_display_links = ('id', )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'notification_id', 'client_id', 'start_datetime', 'end_datetime')
    list_display_links = ('id', )
