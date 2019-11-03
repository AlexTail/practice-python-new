from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
import calendar
from events.models import Events
from events.serializers import EventSerializer
import sqlite3


class BuyTicketsView(APIView):
    def get(self, request):
        one = {"buy_tickets": {
                            "id": "Transaction id",
                            "title": "Title of event",
                            "date": "Date of event",
                            "number": "Number of places",
                            "city": "City"}}
        return Response(one)

    def post(self, request):
        event = request.data.get('buy_tickets')
        number = event['number']
        title = event['title']
        date = event['date']
        city = event['city']
        answer = []
        event = Events.objects.all()
        serializer = EventSerializer(event, many=True)
        for i in serializer.data:
            if i['title'] == title and (i['date'] == date or i['periodicity'].lower() == 'каждый день'
                                        or (i['periodicity'].lower() == 'каждый месяц' and
                                            i['date'].split('-')[2] == date.split('-')[2]) or
                                        (i['periodicity'].lower() == 'каждый год') and
                                        i['date'].split('-')[2] == date.split('-')[2] and
                                        i['date'].split('-')[1] == date.split('-')[1]) and i['city'] == city:
                answer.append(i)
        if len(answer) > 0:
            answer = answer[0]
        else:
            return Response({"Exception": "нет мероприятия на данное время"})
        if int(answer['free_places']) < int(number):
            return Response({"Exception": "закончились места"})

        mydate = answer['date'].split('-')[2] + '.' + answer['date'].split('-')[1] + '.' + answer['date'].split('-')[0]
        workdate = datetime.datetime.strptime(mydate, "%d.%m.%Y")
        ff_day_of_weak = calendar.day_abbr[workdate.date().weekday()]
        answer['date'] = date
        mydate = date.split('-')[2] + '.' + date.split('-')[1] + '.' + date.split('-')[0]
        workdate = datetime.datetime.strptime(mydate, "%d.%m.%Y")
        day_of_weak = calendar.day_abbr[workdate.date().weekday()]
        if ff_day_of_weak == 'Sat' or ff_day_of_weak == 'Sun':
            if day_of_weak != 'Sat' and day_of_weak != 'Sun':
                answer['price'] = str(int(answer['price']) // 2)
        else:
            if day_of_weak == 'Sat' and day_of_weak == 'Sun':
                answer['price'] = str(int(answer['price']) * 2)

        price = answer['price']
        periodicity = answer['periodicity']
        con = sqlite3.connect("./db.sqlite3")
        cur = con.cursor()
        dd = cur.execute("SELECT id from events_events" +
                         ' WHERE date="' + answer['date'] + '" and title="' + title + '"').fetchall()
        maxid = cur.execute("SELECT id from events_events" +
                            ' WHERE id > 0').fetchall()
        new_id = str(int(max(maxid[-1])) + 1)

        if len(dd) == 0:
            fr_pl = answer['free_places']
            places = str(int(fr_pl) - int(number))
            cur.execute("""INSERT INTO events_events(id,title,date,city,free_places,price,periodicity)""" +
                        'VALUES(' + new_id + ',"' + title + '","' + answer['date'] + '","' +
                        city + '","' + places + '","' + price + '","' + periodicity + '")')
            con.commit()
            con.close()
            return

        if len(dd) == 1:
            fr_pl = cur.execute("SELECT free_places from events_events where id = " + str(max(dd[0]))).fetchone()
            fr_pl = max(fr_pl)
        else:
            fr_pl = cur.execute("SELECT free_places from events_events where id = " + str(max(dd[1]))).fetchone()
            fr_pl = max(fr_pl)

        if int(fr_pl) < int(number):
            return Response({"Exception": "закончились места"})

        cur.execute("""UPDATE events_events
                       SET free_places = free_places - """ + number
                       + ' WHERE title = "' + title + '" and date = "'
                       + date + '" and city = "' + city + '" and id = "' + str(max(dd[-1])) + '"')
        con.commit()
        con.close()
        return Response({"success": "Event"})