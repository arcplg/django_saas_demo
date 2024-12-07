from django.shortcuts import render
from .models import SubscriptionPrice

# Create your views here.
def subscription_price_view(request):
    qs = SubscriptionPrice.objects.filter(featured=True)
    monthly_qs = qs.filter(interval=SubscriptionPrice.InterValChoices.MONTHLY)
    year_qs = qs.filter(interval=SubscriptionPrice.InterValChoices.YEARLY)
    return render(request, "subscriptions/pricing.html", {
        "monthly_qs": monthly_qs,
        "year_qs": year_qs,
    })