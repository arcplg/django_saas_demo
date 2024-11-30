from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from apps.visits.models import PageVisit

User = get_user_model()

# Create your views here.
@login_required
def profile_list_view(request):
    context = {
        "object_list": User.objects.filter(is_active=True)
    }
    return render(request, "profiles/list.html", context)

@login_required
def profile_detail_view(request, username=None, *args, **kwargs):
    user = request.user # user login
    user_groups = user.groups.all()
    if user_groups.filter(name__icontains='basic').exists():
        return HttpResponse("Congrats")
    print(
        user.has_perm("subscriptions.basic"),
        user.has_perm("subscriptions.basic_ai"),
        user.has_perm("subscriptions.pro"),
        user.has_perm("subscriptions.advanced"),    
        user.has_perm("apps.visits.view_pagevisit"),    
    )
    # <app_label>.view_<model_name>
    # <app_label>.add_<model_name>
    # <app_label>.change_<model_name>
    # <app_label>.delete_<model_name>

    # profile = User.objects.get(username=username)
    profile = get_object_or_404(User, username=username)
    is_me = profile == user
    # if is_me:
    #     if user.has_perm("apps.visits.view_pagevisit"):
    #         # qs = PageVisit.objects.all()
    #         pass

    context = {
        "object": profile,
        "instance": profile,
        "owner": is_me
    }
    return render(request, "profiles/detail.html", context)
