from django.urls import path
from . import views

urlpatterns = [
    path('pricing/', views.subscription_price_view, name='subscriptions.pricing'),
    path('pricing/<str:interval>/', views.subscription_price_view, name='subscriptions.pricing_interval'),
    path('billing/', views.user_subscription_view, name='subscriptions.billing'),
    path('cancel-billing/', views.user_subscription_cancel_view, name='subscriptions.cancel_billing')
]