# -*- coding: utf-8 -*-
# !/usr/bin/python3
import requests
from bs4 import BeautifulSoup as BS
import codecs

__all__ = ('work', 'rabota', 'dou', 'djinni', 'get_html')

headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}  # имуляция действия поведения браузера



def get_html(url):
    session = requests.Session()  # непрерывность действия во времени (имитация человека)
    request = session.get(url, headers=headers)  # имуляция открытия странички в браузере

    return request.content


def work(html):
    jobs = []
    errors = []
    domain = 'https://www.work.ua'

    if html:
        soup = BS(html, 'lxml')
        main_div = soup.find('div', id="pjax-job-list")
        if main_div:
            div_list = main_div.find_all('div', attrs={'class': 'job-link'})
            for div in div_list:
                title = div.find('h2')
                href = domain + title.a['href']
                content = div.p.text
                company = 'No name'
                logo = div.find('img')
                if logo:
                    company = logo['alt']

                jobs.append({
                    'title': title.text,
                    'url': href,
                    'description': content,
                    'company': company,
                })
            else:
                errors.append({'url': href, 'title': 'div does not exists'})
    else:
        errors.append({'url': url, 'title': 'page do not response'})

    return jobs, errors


def rabota(html):
    jobs = []
    errors = []
    domain = 'https://rabota.ua'

    if html:
        soup = BS(html, 'lxml')
        main_div = soup.find('table', id="ctl00_content_ctl00_gridList")
        if main_div:
            div_list = main_div.find_all('tr', attrs={'id': True})
            for div in div_list:
                card_content = div.find('div', attrs={'class': 'card-main-content'}).find('div', attrs={
                    'class': 'common-info'})

                title = card_content.find('p', attrs={'class': 'card-title'})
                href = domain + title.a['href']
                content = div.find('div', attrs={'class': 'card-description'}).text
                company = card_content.find('p', attrs={'class': 'company-name'}).text

                jobs.append({
                    'title': title.text,
                    'url': href,
                    'description': content,
                    'company': company,
                })
        else:
            errors.append({'url': href, 'title': 'div does not exists'})
    else:
        errors.append({'url': url, 'title': 'page do not response'})

    return jobs, errors


def dou(html):
    jobs = []
    errors = []

    if html:
        soup = BS(html, 'lxml')
        main_div = soup.find('div', id="vacancyListId")
        if main_div:
            li_list = main_div.find_all('div', attrs={'_id': True})
            for div in li_list:
                div_title = div.find('div', attrs={'class': 'title'})

                title = div_title.a
                href = title['href']
                content = div.find('div', attrs={'class': 'sh-info'}).text
                company = div_title.find('a', attrs={'class', 'company'})

                jobs.append({
                    'title': title.text,
                    'url': href,
                    'description': content,
                    'company': company.text,
                })
        else:
            errors.append({'url': href, 'title': 'div does not exists'})
    else:
        errors.append({'url': url, 'title': 'page do not response'})

    return jobs, errors


def djinni(html):
    jobs = []
    errors = []
    domain = 'https://djinni.co/'

    if html:
        soup = BS(html, 'lxml')
        div_list = soup.find('section', attrs={'class': 'jobs-list-wrapper'})
        if div_list:
            for div in div_list:
                art = div.find('article', attrs={'class': 'svelte-184g0n'})

                title = art.find('p', attrs={'class': 'title'})
                href = domain + title.a['href']
                content = art.find_all('p', attrs={'class': 'svelte-184g0n'})[-1].get_text(strip=True)
                company = title.find('span', attrs={'class': 'company'})

                jobs.append({
                    'title': title.a.text,
                    'url': href,
                    'description': content,
                    'company': company,
                })
        else:
            errors.append({'url': href, 'title': 'div does not exists'})
    else:
        errors.append({'url': url, 'title': 'page do not response'})

    return jobs, errors


def main():
    html_work = get_html('https://www.work.ua/jobs-kyiv-python/')
    html_rabota = get_html(
        'https://rabota.ua/jobsearch/vacancy_list?regionId=1&keyWords=python&period=2&lastdate=05.07.2020')
    html_dou = get_html('https://jobs.dou.ua/vacancies/?category=Python&search=Киев')
    html_djinni = get_html('https://djinni.co/jobs2/?category=python&location=kyiv&')

    print(djinni(html_djinni))

    h = codecs.open('parser.txt', 'w', 'utf-8')
    h.write(str(djinni(html_djinni)))


if __name__ == '__main__':
    main()
