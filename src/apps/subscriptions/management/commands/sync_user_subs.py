import helpers.billing
from typing import Any
from django.core.management.base import BaseCommand

from apps.subscriptions.models import UserSubscription
from apps.customers.models import Customer

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        qs = Customer.objects.filter(stripe_id__isnull=False)
        for customer_obj in qs:
            user = customer_obj.user
            customer_stripe_id = customer_obj.stripe_id
            print(f"Sync {user} - {customer_stripe_id} subs and remove old ones")
            subs = helpers.billing.get_customer_active_subscription(customer_stripe_id)
            for sub in subs:
                existing_user_subs_qs = UserSubscription.objects.filter(stripe_id__iexact=f"{sub.id}".strip())
                if existing_user_subs_qs.exists():
                    continue
                helpers.billing.cancel_subscription(sub.id, reason="Dangling active subscription", cancel_at_period_end=False)
                # print(sub.id, existing_user_subs_qs.exists())

            