from django.urls import re_path
from mailing_service.views import ClientListAPIView, ClientAPIView, NotificationListAPIView, NotificationAPIView, \
    MessageListByNotificationAPIView, MessagesCountGroupByStatusAPIView

urlpatterns = [
    re_path(r'^clients/?$', ClientListAPIView.as_view(), name='client-list-view'),
    re_path(r'^clients/(?P<pk>[0-9]*)/?$', ClientAPIView.as_view(), name='client_detail_view'),
    re_path(r'^notifications/?$', NotificationListAPIView.as_view(), name='notification-list-view'),
    re_path(r'^notifications/messages/?$', MessagesCountGroupByStatusAPIView.as_view(), name='message-stats-view'),
    re_path(r'^notifications/(?P<pk>[0-9]*)/?$', NotificationAPIView.as_view(), name='notification-detail-view'),
    re_path(r'^notifications/(?P<pk>[\d]*)/messages/?$', MessageListByNotificationAPIView.as_view(),
            name='message-list-by-notification-view'),
]
