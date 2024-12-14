import helpers.billing
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from apps.subscriptions.models import SubscriptionPrice, Subscription, UserSubscription
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponseBadRequest

User = get_user_model()
BASE_URL = settings.BASE_URL

# Create your views here.
def product_price_redirect_view(request, price_id=None, *args, **kwargs):
    request.session['checkout_subscription_price_id'] = price_id
    return redirect("checkout.stripe-checkout-start")

@login_required
def checkout_redirect_view(request):
    checkout_subscription_price_id = request.session.get("checkout_subscription_price_id")
    try:
        obj = SubscriptionPrice.objects.get(id=checkout_subscription_price_id)
    except:
        obj = None
    if checkout_subscription_price_id is None or obj is None:
        return redirect("subscriptions.pricing")
    customer_stripe_id = request.user.customer.stripe_id
    success_url_path = reverse("checkout.stripe-checkout-success")
    cancel_url_path = reverse("subscriptions.pricing")
    success_url = f"{BASE_URL}{success_url_path}"
    cancel_url = f"{BASE_URL}{cancel_url_path}"
    price_stripe_id = obj.stripe_id
    url = helpers.billing.start_checkout_session(
        customer_stripe_id,
        success_url=success_url,
        cancel_url=cancel_url,
        price_stripe_id=price_stripe_id,
        raw=False
    )
    return redirect(url)

def checkout_success_view(request):
    session_id = request.GET.get('session_id')
    customer_id, plan_id = helpers.billing.get_checkout_customer_plan(session_id)
    price_qs = SubscriptionPrice.objects.filter(stripe_id=plan_id)
    # get subscription object
    try:
        sub_obj = Subscription.objects.get(subscriptionprice__stripe_id=plan_id)
    except:
        sub_obj = None
    # get user object
    try:
        user_obj = User.objects.get(customer__stripe_id=customer_id)
    except:
        user_obj = None
    # get user subscription object
    _user_sub_exists = False
    try:
        _user_sub_obj = UserSubscription.objects.get(user=user_obj)
        _user_sub_exists = True
    except UserSubscription.DoesNotExist:
        _user_sub_obj = UserSubscription.objects.create(user=user_obj, subscription=sub_obj)
    except:
        _user_sub_obj = None
    if None in [sub_obj, user_obj, _user_sub_obj]:
        return _user_sub_obj("There was an error with your account, please contact us.")
    if _user_sub_exists:
        # cancel old sub
        # assign new sub
        _user_sub_obj.subscription = sub_obj
        _user_sub_obj.save()
    context = {}
    return render(request, "checkouts/success.html", context)