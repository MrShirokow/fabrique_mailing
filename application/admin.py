from django.contrib import admin

from application.entities.client.model import Client
from application.entities.message.model import Message
from application.entities.notification.model import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_datetime', 'end_datetime')
    list_display_links = ('id', 'start_datetime', 'end_datetime')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'mobile_operator_code', 'tag', 'time_zone')
    list_display_links = ('id', 'phone_number')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'notification_id', 'client_id', 'sending_datetime', 'is_send')
    list_display_links = ('id', )
