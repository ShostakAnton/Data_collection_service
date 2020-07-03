from django.shortcuts import render
from .models import Vacancy, City


def home_view(request):
    qs = Vacancy.objects.all()
    return render(request, 'scraping/home.html', {'object_list': qs})
