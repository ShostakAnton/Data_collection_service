import os, sys

proj = os.path.dirname(os.path.abspath('manage.py'))  # абсолютный путь к проекту
sys.path.append(proj)  # добавление пути в системные переменные путей
os.environ['DJANGO_SETTINGS_MODULE'] = "Data_collection_service.settings"  # установка настроек

import django

django.setup()

from django.db import DatabaseError
from scraping.parser_my import *
from scraping.models import Vacancy, City, Language

parsers = (
    (work, 'https://www.work.ua/jobs-kyiv-python/'),
    (dou, 'https://jobs.dou.ua/vacancies/?category=Python&search=Киев'),
    (djinni, 'https://djinni.co/jobs2/?category=python&location=kyiv&'),
    (rabota, 'https://rabota.ua/jobsearch/vacancy_list?regionId=1&keyWords=python&period=2&lastdate=05.07.2020')
)
city = City.objects.filter(slug='kiev').first()
language = Language.objects.filter(slug='python').first()
jobs, errors = [], []

for func, url in parsers:
    j, e = func(get_html(url))
    jobs += j
    errors += e

k = 0
for job in jobs:
    k += 1
    print(k)
    v = Vacancy(title=job['title'],
                url=job['url'],
                description=job['description'],
                company=job['company'],
                city=city,
                language=language)

    try:
        v.save()
    except:
        pass
