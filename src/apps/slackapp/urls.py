from django.urls import path
from . import views

urlpatterns = [
    path("oauth_request", views.slack_oauth_request),
    path("callback", views.slack_callback),
    path("callback/success", views.slack_callback_success),
    path("events", views.slack_events)
]