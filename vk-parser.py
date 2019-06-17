"""
Парсер данных со стены в группе вконтакте с API vk

Пофиксить: Когда в windows, то редко post['text'] содержит '\u200b\200b'
и т.д., исключение появляется и не записываются данные в csv
"""

import csv
import time
import requests
from chardet.universaldetector import UniversalDetector


def take_1000_posts():
    """Возвращает список постов (до 1000 шт). Идёт обращение к API vk"""
    token = 'e9d3bafee9d3bafee9d3bafe8ce9b949c5ee9d3e9d3bafeb525d23efe748e5a8170cc3e'
    version = 5.95
    domain = 'vcru'
    count = 100
    offset = 0
    all_posts = []

    while offset < 1000:
        response_vk = requests.get('https://api.vk.com/method/wall.get',
                                    params={
                                        'access_token': token,
                                        'v': version,
                                        'domain': domain,
                                        'count' : count,
                                        'offset' : offset
                                    }
                                    )
        data = response_vk.json()['response']['items']
        offset += 100
        all_posts.extend(data)
        time.sleep(0.5)
    return all_posts


def file_writer(data):
    """Создание файла csv и запись в него данных, извлеченных из (data)"""
    with open('vcru.csv', 'w') as file: # encoding='cp1251' or 'utf8'
        a_pen = csv.writer(file, delimiter=';')
        a_pen.writerow(('№', 'likes', 'body', 'url'))
        num = 1
        er_num = 0
        url_video = 'https://vk.com/video'
        
        for post in data:
            try:
                if post['attachments'][0]['type'] == 'link':
                    img_url = post['attachments'][0]['link']['photo']['sizes'][0]['url']
                
                elif post['attachments'][0]['type'] == 'photo':
                    img_url = post['attachments'][0]['photo']['sizes'][-1]['url']
                
                elif post['attachments'][0]['type'] == 'doc':
                    img_url = post['attachments'][0]['doc']['url']
                    
                elif post['attachments'][0]['type'] == 'video':
                    img_url = url_video  + \
                              str(post['attachments'][0]['video']['owner_id']) + \
                              '_' + str(post['attachments'][0]['video']['id'])
                else:
                    img_url = 'Пусто'
                    print('Не нашел картинку/gif/видео у номера:', num-1)
                a_pen.writerow((num, post['likes']['count'], post['text'], img_url))
                
            except Exception as ex:
                print('Исключение у строки:', num-1, ex)
                er_num += 1
            num += 1
    print('Количество исключений (не записанных строк в csv): ', er_num)
    print(f'В файл csv, успешно записались: {str(len(posts)-er_num)} строк')
    
posts = take_1000_posts()
file_writer(posts)
print(f'Изначально полученный список: {str(len(posts))} строк')
print('done')
