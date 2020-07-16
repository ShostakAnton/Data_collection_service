import os, sys
import django
import datetime
from django.core.mail import EmailMultiAlternatives

from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))  # абсолютный путь к проекту
sys.path.append(proj)  # добавление пути в системные переменные путей
os.environ['DJANGO_SETTINGS_MODULE'] = "Data_collection_service.settings"  # установка настроек

django.setup()
from scraping.models import Vacancy, Error
from Data_collection_service.settings import EMAIL_HOST_USER

ADMIN_USER = EMAIL_HOST_USER

today = datetime.date.today()  # текущая дата

subject = f"Рассылка вакансий за {today}"
text_content = f"Рассылка вакансий за {today}"
from_email = EMAIL_HOST_USER

empty = '<h2>К сожалению на сегодня по Вашим предпочтениям данных нет. </h2>'


User = get_user_model()  # создание модели юзера

qs = User.objects.filter(send_email=True).values('city',
                                                 'language',
                                                 'email')  # получаем яп/город/почту у всех пользователей у которых стоит рассылка писем
users_dct = {}
for i in qs:
    users_dct.setdefault((i['city'], i['language']), [])
    users_dct[(i['city'], i['language'])].append(
        i['email'])  # {('odessa', 'python'): ['email@gmail.com'], ('kiev', 'js'): ['email1@gmail.com']}

if users_dct:
    params = {'city_id__in': [],
              'language_id__in': []}  # __in - говорит о том, что нужно найти все значения, которые принадлежат этой паре
    for pair in users_dct.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(
            pair[1])  # {'city_id__in': ['odessa', 'kiev'], 'language_id__in': ['python', 'js']}
    qs = Vacancy.objects.filter(**params, timestamp=today).values()
    vacancies = {}
    # for i in qs:
    #     vacancies.setdefault((i['city_id'], i['language_id']), [])
    #     vacancies[(i['city_id'],
    #                i['language_id'])].append(
    #         i)  # {(1, 2): [{'id': 482, 'url': 'https://www.work.ua/jobs/3933377/', 'title': '\nMiddle C++/Python developer\n', 'company': 'Playson', ...
    # for keys, emails in users_dct.items():  # формирование html письма
    #     rows = vacancies.get(keys, [])
    #     html = ''
    #     for row in rows:
    #         html += f'<h5"><a href="{row["url"]}">{row["title"]}</a></h5>'
    #         html += f'<p>{row["description"]} </p>'
    #         html += f'<p>{row["company"]} </p><br><hr>'
    #     _html = html if html else empty
    #     for email in emails:  # рассылка писем
    #         to = email
    #         msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    #         msg.attach_alternative(_html, "text/html")
    #         msg.send()

# subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
# text_content = 'This is an important message.'
# html_content = '<p>This is an <strong>important</strong> message.</p>'
# msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
# msg.attach_alternative(html_content, "text/html")
# msg.send()


qs = Error.objects.filter(timestamp=today)      # получение ошибок
if qs.exists():     # exists() полезен для определения нахождения объекта в QuerySet и наличия какого-либо объекта в QuerySet, особенно для больших QuerySet
    error = qs.first()
    data = error.data
    _html = ''
    for i in data:
        _html += f'<p"><a href="{ i["url"] }">Error: { i["title"] }</a></p><br>'
    subject = f"Ошибки скрапинга {today}"
    text_content = "Ошибки скрапинга"
    to = ADMIN_USER
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()
