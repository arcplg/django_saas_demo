import helpers.billing
from django.shortcuts import render, redirect
from .models import SubscriptionPrice, UserSubscription
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def user_subscription_view(request, *args, **kwargs):
    user_sub_obj, created = UserSubscription.objects.get_or_create(user=request.user)
    if request.method == "POST":
        print("refresh sub")
        if user_sub_obj.stripe_id:
            sub_data = helpers.billing.get_subscription(user_sub_obj.stripe_id, raw=False)
            for k,v in sub_data.items():
                setattr(user_sub_obj, k, v)
            user_sub_obj.save()
        return redirect(user_sub_obj.get_absolute_url())
    context = {
        "subscription": user_sub_obj
    }
    return render(request, "subscriptions/user_detail_view.html", context)    

def subscription_price_view(request, interval="month"):
    qs = SubscriptionPrice.objects.filter(featured=True)
    inv_mo = SubscriptionPrice.InterValChoices.MONTHLY
    inv_yr = SubscriptionPrice.InterValChoices.YEARLY
    url_path_name = "subscriptions.pricing_interval"
    mo_url = reverse(url_path_name, kwargs={"interval": inv_mo})
    yr_url = reverse(url_path_name, kwargs={"interval": inv_yr})
    active = inv_mo
    if interval == inv_yr:
        active = inv_yr
        interval = inv_yr
    object_list = qs.filter(interval=interval)
    return render(request, "subscriptions/pricing.html", {
        "object_list": object_list,
        "mo_url": mo_url,
        "yr_url": yr_url,
        "active": active
    })