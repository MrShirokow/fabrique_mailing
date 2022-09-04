from django.urls import re_path
from application.views import ClientListAPIView, ClientAPIView, NotificationListAPIView, NotificationAPIView, \
                              MessageListByNotificationAPIView, MessagesCountGroupByStatusAPIView


urlpatterns = [
    re_path(r'^clients/?$', ClientListAPIView.as_view()),
    re_path(r'^clients/(?P<pk>[0-9]*)/?$', ClientAPIView.as_view()),
    re_path(r'^notifications/?$', NotificationListAPIView.as_view()),
    re_path(r'^notifications/messages/?$', MessagesCountGroupByStatusAPIView.as_view()),
    re_path(r'^notifications/(?P<pk>[0-9]*)/?$', NotificationAPIView.as_view()),
    re_path(r'^notifications/(?P<pk>[\d]*)/messages/?$', MessageListByNotificationAPIView.as_view()),
]
