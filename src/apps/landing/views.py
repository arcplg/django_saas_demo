import helpers.numbers
from django.shortcuts import render
from apps.visits.models import PageVisit
from apps.dashboard.views import dashboard_view

# Create your views here.

def landing_page_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        return dashboard_view(request)
    query = PageVisit.objects.all()
    PageVisit.objects.create(path=request.path)
    page_view_formatted = helpers.numbers.shorten_number(query.count() * 100_000)
    social_view_formatted = helpers.numbers.shorten_number(query.count() * 23_000)
    context = {
        "page_view_count": page_view_formatted,
        "social_view_count": social_view_formatted
    }
    return render(request, "landing/main.html", context)