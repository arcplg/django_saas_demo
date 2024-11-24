from django.urls import path
from . import views

urlpatterns = [
    path('app_demo/', views.app_view, name="app_view"),
]