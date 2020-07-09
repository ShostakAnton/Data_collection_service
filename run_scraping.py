import os, sys

from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))  # абсолютный путь к проекту
sys.path.append(proj)  # добавление пути в системные переменные путей
os.environ['DJANGO_SETTINGS_MODULE'] = "Data_collection_service.settings"  # установка настроек

import django

django.setup()

from django.db import DatabaseError
from scraping.parser_my import *
from scraping.models import Vacancy, City, Language, Error, Url

User = get_user_model()     # ф-ция get_user_model возвращает того польщователя, который опрделен в настройка django проекта

parsers = (
    (work, 'work'),
    (dou, 'dou'),
    (djinni, 'djinni'),
    (rabota, 'rabota')
)

def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst

def get_urls(_settings):
    # получение уникальных urls
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = url_dct[pair]
        urls.append(tmp)
    return urls


settings = get_settings()
url_list = get_urls(settings)

# city = City.objects.filter(slug='kiev').first()
# language = Language.objects.filter(slug='python').first()

jobs, errors = [], []

for data in url_list:

    for func, key  in parsers:
        url = data['url_data'][key]
        j, e = func(get_html(url), city=data['city'], language=data['language'])
        jobs += j
        errors += e

k = 0
for job in jobs:
    k += 1
    print(k)
    v = Vacancy(**job)
    try:
        v.save()
    except:
        print(k, "не получилось")

    if errors:
        er = Error(data=errors).save()
