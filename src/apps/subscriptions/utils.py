import helpers.billing

from django.db.models import Q
from apps.subscriptions.models import UserSubscription, Subscription, SubscriptionStatus
from apps.customers.models import Customer

def refresh_active_users_subscriptions(
        user_ids=None,
        active_only=True,
        days_left=0,
        days_ago=0,
        days_start=0,
        days_end=0,
        verbose=False
    ):
    # user_id=models.For
    # qs = UserSubscription.objects.all()
    # active_qs_lookup = (
    #     Q(status = SubscriptionStatus.ACTIVE) |
    #     Q(status = SubscriptionStatus.TRIALING)
    # )
    qs = UserSubscription.objects.all()
    if active_only:
        qs = qs.by_active_trialing()
    if user_ids is not None:
        qs = qs.by_user_ids(user_ids=user_ids)
    print(days_ago)
    if days_ago > 0:
        qs = qs.by_days_ago(days_ago=days_ago)
    if days_left > 0:
        qs = qs.by_days_left(days_left=days_left)
    if days_start > 0 and days_end > 0:
        qs = qs.by_range(days_start=days_start, days_end=days_end)
    # active_qs = qs.filter(active = SubscriptionStatus.ACTIVE)
    # trialing_qs = qs.filter(active = SubscriptionStatus.TRIALING)
    # qs = (active_qs | trialing_qs)
    # if isinstance(user_ids, list):
    #     qs = qs.filter(user_id__in=user_ids)
    # elif isinstance(user_ids, int):
    #     qs = qs.filter(user_id__in=[user_ids])
    # elif isinstance(user_ids, str):
    #     qs = qs.filter(user_id__in=[user_ids])
    # qs = UserSubscription.objects.get_queryset(user_ids=user_ids)
    complete_count = 0
    qs_count = qs.count()
    print(qs_count)
    for obj in qs:
        if verbose:
            print("Updating user", obj.user, obj.subscription, obj.current_period_end)
        if obj.stripe_id:
            sub_data = helpers.billing.get_subscription(obj.stripe_id, raw=False)
            for k,v in sub_data.items():
                setattr(obj, k, v)
            obj.save()
            complete_count += 1
    return complete_count == qs_count

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

            