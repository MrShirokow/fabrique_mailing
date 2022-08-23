from django.urls import re_path
from application.views import ClientListAPIView


urlpatterns = [
    re_path(r'^clients/?$', ClientListAPIView.as_view()),
    # re_path(r'^themes/(?P<theme_id>[0-9]*)/?$', ThemeDetailView.as_view()),
    # re_path(r'^levels/?$', LevelDetailView.as_view()),
    # re_path(r'^categories/?$', CategoryListView.as_view()),
    # re_path(r'^words/?$', WordListView.as_view()),
    # re_path(r'^words/(?P<word_id>[0-9]*)/?$', WordDetailView.as_view())
]
