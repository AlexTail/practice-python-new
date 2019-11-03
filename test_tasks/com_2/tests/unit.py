import requests
import json
import time
from random import randint as r

get_info = [{"get_info": {"city": "Москва"}},
            {"get_info": {"city": "Пермь"}},
            {"get_info": {"title": "1", "month": "11"}},
            {"get_info": {"title": "2", "month": "10"}},
            {"get_info": {"title": "oneTwo", "month": "12"}},
            {"get_info": {"title": "1", "month": "1"}}]

buy_tickets = [{"buy_tickets": {"id": "1", "title": "1",
                                "date": "2019-10-17", "number": "10", "city": "Пермь"}},
               {"buy_tickets": {"id": "2", "title": "1",
                                "date": "2019-10-31", "number": "1001", "city": "Москва"}},
               {"buy_tickets": {"id": "3", "title": "468",
                                "date": "2019-12-11", "number": "10", "city": "Москва"}},
               {"buy_tickets": {"id": "4", "title": "1",
                                "date": "2019-09-01", "number": "1", "city": "Курск"}}]

new_event = [{"events":{"title": "Star Wars",
                        "date": "2019-2-01",
                        "city": "Реж",
                        "free_places": "100",
                        "price": "400",
                        "periodicity": "каждый месяц"}},
             {"events": {"title": "Nature",
                         "date": "2019-6-18",
                         "city": "Новгород",
                         "free_places": "150",
                         "price": "700",
                         "periodicity": "каждый год"}},
             {"events": {"title": "Егор крид",
                         "date": "2019-5-14",
                         "city": "Париж",
                         "free_places": "50",
                         "price": "500",
                         "periodicity": "каждый день"}},
             {"events": {"title": "3",
                         "date": "2019-8-23",
                         "city": "Берлин",
                         "free_places": "30",
                         "price": "600",
                         "periodicity": "разово"}},
             ]


def main():
    headers = {'content-type': 'application/json'}
    for i in range(6):
        if i < 2:
            tr = new_event[r(0, 3)]
            url = "http://127.0.0.1:8000/api/events/"
        elif i < 4:
            tr = buy_tickets[r(0, 3)]
            url = "http://127.0.0.1:8000/api/buytickets/"
        else:
            tr = get_info[r(0, 3)]
            url = "http://127.0.0.1:8000/api/getinfo/"
        response = requests.post(
            url, data=json.dumps(tr), headers=headers).json()
        if response:
            print('True')
    print('-> Success!')
    time.sleep(60)


if __name__ == "__main__":
    main()