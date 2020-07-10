from django.shortcuts import render
from .models import Vacancy, City
from .forms import FindForm
from django.core.paginator import Paginator


def home_view(request):
    form = FindForm()

    return render(request, 'scraping/home.html', {'form': form})


def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')


    context = {'city': city, 'language': language, 'form': form }
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language

        qs = Vacancy.objects.filter(**_filter)

        paginator = Paginator(qs, 10)
        page = request.GET.get("page")  # получаем номер страницы на которой сейчас находимя\ся
        page_obj = paginator.get_page(page)
        context['object_list'] = page_obj
    return render(request, 'scraping/list.html', context)
