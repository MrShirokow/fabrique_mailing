from django.contrib import admin

from application.entities.client import Client
from application.entities.message import Message
from application.entities.notification import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_datetime', 'end_datetime', 'text', 'sending_filter')
    list_display_links = ('id', 'text')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'mobile_operator_code', 'tag', 'time_zone')
    list_display_links = ('id', 'phone_number')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'notification_id', 'client_id', 'sending_datetime', 'is_sending')
    list_display_links = ('id', )
