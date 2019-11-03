import requests
import json
import time


def main():

    headers = {'content-type': 'application/json'}
    print('(1) Добавить мероприятие (2) Список мероприятий в городе (3) О мероприятии в определенный месяц (4) Купить билет')
    inp = input()
    if '1' in inp.lower():
        ans = create()
        url = "http://127.0.0.1:8000/api/events/"
    elif '2' in inp.lower():
        ans = city()
        url = "http://127.0.0.1:8000/api/getinfo/"
    elif '3' in inp.lower():
        ans = event()
        url = "http://127.0.0.1:8000/api/getinfo/"
    else:
        ans = buy_ticket()
        url = "http://127.0.0.1:8000/api/buytickets/"  

    response = requests.post(
        url, data=json.dumps(ans), headers=headers).json() 
    if '1' in inp.lower():
        print(response['success'])
    elif '2' in inp.lower():
        for i in response['events']:
            print('Название - ' + i ['title'])
            print('Дата - ' + i ['date'])
            print('Свободные места - ' + i ['free_places'])
            print('Цена билета - ' + i ['price'])
            print('Периодичность - ' + i ['periodicity'])
            print('==================================================')
    elif '3' in inp.lower():
        for i in response['events']:
            print('Название - ' + i['title'])
            print('Дата - ' + i['date'])
            print('Город - ' + i['city'])
            print('Свободные места - ' + i['free_places'])
            print('Цена билета - ' + i['price'])
            print('Периодичность - ' + i['periodicity'])
            print('==================================================')
    else:
        print(response)
    time.sleep(60)


def city():
    print('Город:')
    town = input()
    
    req = {
        "get_info": {
            "city": town
        }
    }
    return req


def event():
    print('Название мероприятия')
    title = input()
    print('Месяц(число)')
    month = input()
    req = {
        "get_info": {
            "title": title,
            "month": month
        }
    }
    return req


def create():
    print('Название мероприятия')
    title = input()
    print('Дата(ГГ-ММ-ДД)')
    date = input()
    print('Город')
    city = input().title()
    print('Количество свободных мест')
    free_places = input()
    print('Цена билета')
    price = input()
    print('Периодичность мероприятия (каждый день/каждый месяц/каждый год/разово)')
    periodicity = input()

    req = {
        "events": {
            "title": title,
            "date": date,
            "city": city,
            "free_places": free_places,
            "price": price,
            "periodicity": periodicity
        }
    }
    return req


def buy_ticket():
    print('Название мероприятия')
    title = input()
    print('Дата(ГГ-ММ-ДД)')
    date = input()
    print('Город')
    city = input().title()
    print('Количество билетов')
    num_places = input()
    print('Id операции')
    transaction_id = input()
    req = {
        "buy_tickets": {
            "id": "Transaction id",       # transaction_id
            "title": title,
            "date": date,
            "number": num_places,
            "city": city
        }
    }
    return req


if __name__ == "__main__":
    main()