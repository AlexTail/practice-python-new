"""

RU: Парсер, который получает с сайта https://habr.com/ru/ самые
популярные посты за год. 

ENG: A parser that receives from the site https://habr.com/ru/
the most popular posts of the year.

"""


import requests
from bs4 import BeautifulSoup as bs
import csv


headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
          }

base_url = 'https://habr.com/ru/top/yearly/page1/'

def habr_parse(base_url, headers):

    posts = []
    urls = []

    session = requests.Session()
    request = session.get(base_url, headers=headers)
    page = 0
    
    if request.status_code == 200:
        print(f'Status_code: {request.status_code}')
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find('a', attrs={'class' : 'toggle-menu__item-link toggle-menu__item-link_pagination toggle-menu__item-link_bordered'})
            count_pages = int(pagination['href'][19:-1])
            
            last_page_url = 'https://habr.com' + pagination['href']
           
            def number_of_posts_on_the_page(url, head):
                request = session.get(url, headers=head)
                soup = bs(request.content, 'lxml')
                number_of_posts_on_the_page = soup.findAll('article', attrs={'class' : 'post'})
                return len(number_of_posts_on_the_page) 

            first_page = number_of_posts_on_the_page(base_url, headers)
            last_page = number_of_posts_on_the_page(last_page_url, headers)

            def sum_posts(p_first, p_last, p_quantity):
                """ Кол-во постов на всех страницах за 1 год (лучшие) """
                return p_first * (p_quantity - 1) + p_last
            
            all_posts = int(sum_posts(first_page, last_page, count_pages))
            
            print('Кол-во постов на сайте: ', all_posts)
            print('Кол-во постов, которое запросил пользователь: ', required_amount)
       
            def exit_program():
                if int(required_amount) < 1 or int(required_amount) > all_posts:
                    print('Вы ввели неправильное кол-во постов для парсинга. Перезапустите программу ' + \
                    'и введите число от 1 до', all_posts)
                    sys.exit()
                
            exit_program()

            def search_range(got_user_posts, first_page_posts):
                to_range = int(required_amount) / first_page
                if got_user_posts % first_page_posts == 0:
                    to_range = int(to_range)
                else:
                    to_range = int(to_range)+1
                return to_range
                
            print('Кол-во страниц для парсинга:', search_range(int(required_amount), first_page))
                
            diapason = search_range(int(required_amount), first_page)
     
            for i in range(diapason):
                url = f'https://habr.com/ru/top/yearly/page{i+1}/'
                if url is not urls:
                    urls.append(url)
        except:
            pass
        
        for url in urls:
            request = session.get(url, headers=headers)
            soup = bs(request.content, 'lxml')
            divs = soup.findAll('article', attrs={'class' : 'post'})
            page += 1
            
            for div in divs:
                num = 0
                if len(posts) != int(required_amount): 
                    try:
                        title = div.find('a', attrs={'class' : 'post__title_link'}).text
                        description = div.find('div', attrs={'class' : 'js-mediator-article'}).text
                        description_in_one_line = " ".join(description.split())
                        date = div.find('span', attrs={'class' : 'post__time'}).text
                        name = div.find('span', attrs={'class' : 'user-info__nickname'}).text
                        
                        posts.append({
                            'Заголовок поста': title,
                            'Короткое описание поста': description_in_one_line,
                            'Дата публикации': date,
                            'Имя автора поста': name
                        })
                        num += 1
                      
                    except Exception as ex:
                        print(f'Исключение: {ex}')
                        print('Страница с исключением в браузере №', int(url[-2:].replace('=', '')) + 1) # актуально в браузере для 1-99 стр.
                        print(f'Пост на странице в браузере № {num+1}', '\n')
                else:
                    break
               
            print(f'Спарсилась страница в браузере № {page}')    
        if posts:
            print('Получено и сохранено в таблицу, постов: ', len(posts), '\n')
    else:
        print(f'Error or Done. Status_code: {request.status_code}')
    return posts    




def file_writer(posts):
    with open('parced_habr.csv', 'w') as file:
        a_pen = csv.writer(file, delimiter=';')
        a_pen.writerow(('№', 'Заголовок поста', 'Короткое описание поста', 'Дата публикации', 'Имя автора поста'))
        num = 1
        isk = 0
        for post in posts:
            try:
                a_pen.writerow((num, post['Заголовок поста'], post['Короткое описание поста'], post['Дата публикации'], post['Имя автора поста']))
            except Exception as ex:
                isk += 1
            num += 1




if __name__ == "__main__":
    required_amount = input('Введите кол-во постов для парсинга: ')
    posts = habr_parse(base_url, headers)
    file_writer(posts)
    print('Done')