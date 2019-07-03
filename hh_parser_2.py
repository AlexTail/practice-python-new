"""

Парсер вакансий с сайта hh.ru (без учёта рекламных предложений)

Parser vacancies from the site hh.ru (excluding promotional offers)

"""


import requests
from bs4 import BeautifulSoup as bs
import csv


headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' + \
           'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
          }
base_url = 'https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&search_period=7&text=Python&from=cluster_area&page=0'


def hh_parse(base_url, headers):
    jobs = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    page = 0
    if request.status_code == 200:
        print(f'Status_code: {request.status_code}')
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.findAll('a', attrs={'data-qa' : 'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f'https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&search_period=7&text=Python&from=cluster_area&page={i}'
                if url is not urls:
                    urls.append(url)
        except:
            pass
        for url in urls:
            request = session.get(url, headers=headers)
            soup = bs(request.content, 'lxml')
            divs = soup.findAll('div', attrs={'data-qa' : 'vacancy-serp__vacancy'})
            page += 1
            
            for div in divs:
                num = 0
                try:
                    title = div.find('a', attrs={'data-qa' : 'vacancy-serp__vacancy-title'}).text
                    href = div.find('a', attrs={'data-qa' : 'vacancy-serp__vacancy-title'})['href']
                    company = div.find('a', attrs={'data-qa' : 'vacancy-serp__vacancy-employer'}).text.strip()
                    text1 = div.find('div', attrs={'data-qa' : 'vacancy-serp__vacancy_snippet_responsibility'}).text
                    text2 = div.find('div', attrs={'data-qa' : 'vacancy-serp__vacancy_snippet_requirement'}).text
                    content = text1 + ' ' + text2
                    jobs.append({
                        'title': title,
                        'href': href,
                        'company': company,
                        'content': content
                    })
                    num += 1
                except Exception as ex:
                    print(f'Исключение: {ex}')
                    print('Страница с исключением в браузере №', int(url[-2:].replace('=', '')) + 1) # актуально в браузере для 1-99 стр.
                    print(f'Объявление на странице в браузере № {num+1}', '\n')
            print(f'Спарсилась страница в браузере № {page}')    
            print('Спарсено объявлений: ', len(jobs), '\n')
    else:
        print(f'Error or Done. Status_code: {request.status_code}')
    return jobs    
 

def file_writer(jobs):
    with open('parced_jobs_hh.csv', 'w') as file:
        a_pen = csv.writer(file, delimiter=';')
        a_pen.writerow(('№', 'Название вакансии', 'Название компании', 'Описание', 'Ссылка'))
        num = 1
        for job in jobs:
            try:
                a_pen.writerow((num, job['title'], job['company'], job['content'], job['href']))
            except Exception as ex:
                print(f'Исключение {ex} у объявления № {num}')
                print(job['title'], job['company'], job['href'], ' ', sep='\n')
            num += 1


jobs_hh = hh_parse(base_url, headers)
file_writer(jobs_hh)
print('done')