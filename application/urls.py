from django.urls import re_path, path
from application.views import ClientListAPIView, ClientAPIView, NotificationListAPIView, NotificationAPIView


urlpatterns = [
    re_path(r'^clients/?$', ClientListAPIView.as_view()),
    re_path(r'^clients/(?P<pk>[0-9]*)/?$', ClientAPIView.as_view()),
    re_path(r'^notifications/?$', NotificationListAPIView.as_view()),
    re_path(r'^notifications/(?P<pk>[0-9]*)/?$', NotificationAPIView.as_view()),
]
