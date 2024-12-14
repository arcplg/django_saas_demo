from django.urls import path
from . import views

urlpatterns = [
    path('sub-price/<int:price_id>', views.product_price_redirect_view, name='checkout.sub-price-checkout'),
    path('start/', views.checkout_redirect_view, name='checkout.stripe-checkout-start'),
    path('success/', views.checkout_success_view, name='checkout.stripe-checkout-success'),
]