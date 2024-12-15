import helpers.billing

from apps.subscriptions.models import UserSubscription, Subscription
from apps.customers.models import Customer

def clear_dangling_subs():
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

def sync_subs_group_permissions():
    qs = Subscription.objects.filter(active=True)
    for obj in qs:
        # print(obj.groups.all())
        sub_perms = obj.permissions.all()
        for group in obj.groups.all():
            group.permissions.set(sub_perms)
            # for per in obj.permissions.all():
            #     group:permissions.add(per)
        # print(obj.permissions.all())

            