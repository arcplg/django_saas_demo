from django.urls import path
from . import views

urlpatterns = [
    path("get-csrf-token", views.get_csrf_token),
    path("send-message", views.send_message)
]