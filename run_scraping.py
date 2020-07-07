from scraping.parser_my import *
import codecs

parsers = (
    (work, 'https://www.work.ua/jobs-kyiv-python/'),
    (dou, 'https://jobs.dou.ua/vacancies/?category=Python&search=Киев'),
    (djinni, 'https://djinni.co/jobs2/?category=python&location=kyiv&'),
    (rabota, 'https://rabota.ua/jobsearch/vacancy_list?regionId=1&keyWords=python&period=2&lastdate=05.07.2020')
)

jobs, errors = [], []
for func, url in parsers:
    j, e = func(get_html(url))
    jobs += j
    errors += e

h = codecs.open('work.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()

