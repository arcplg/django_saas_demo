from django.http import HttpResponse
import pathlib
from django.shortcuts import render
from visits.models import PageVisit

this_dir = pathlib.Path(__file__).resolve().parent

def home_view(request, *args, **kwargs):
    return about_view(request, *args, **kwargs)

def about_view(request, *args, **kwargs):
    ps = PageVisit.objects.all()
    page_ps = PageVisit.objects.filter(path=request.path)
    try:
        percent = (page_ps.count() * 100.0) / ps.count()
    except:
        percent = 0
    my_content = {
        "page_title": 'Page About',
        "page_visit_count": page_ps.count(),
        "percent": percent,
        "total_visit_count": ps.count()
    }
    html_template = "home.html"
    PageVisit.objects.create(path=request.path)
    return render(request, html_template, my_content)