"""
URL configuration for cfehome project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from .views import (
    home_view,
    about_view,
    pw_protected_view,
    user_only_view,
    staff_only_view
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('protected/', pw_protected_view, name='pw_protected_view'),
    path('protected/user-only/', user_only_view, name='user_only_view'),
    path('protected/staff-only/', staff_only_view, name='staff_only_view'),
    path('', include("apps.auth.urls")),
    path('accounts/', include('allauth.urls')),
    path('profiles/', include('apps.profiles.urls')),
    path('', include('apps.demo.urls')),
    path('subscriptions/', include('apps.subscriptions.urls')),
]
