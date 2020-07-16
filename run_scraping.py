import os, sys
import asyncio
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

jobs, errors = [], []

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

async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, get_html(url), city, language)
    errors.extend(err)
    jobs.extend(job)

settings = get_settings()
url_list = get_urls(settings)



loop = asyncio.get_event_loop()         # содание цикла, где будут запускаться наши задачи
tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
             for data in url_list
             for func, key  in parsers]        # список задач
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])     # выполнение указаных задач

# for data in url_list:
#
#     for func, key  in parsers:
#         url = data['url_data'][key]
#         j, e = func(get_html(url), city=data['city'], language=data['language'])
#         jobs += j
#         errors += e

loop.run_until_complete(tasks)
loop.close()


for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except:
        pass

    if errors:
        er = Error(data=errors).save()
