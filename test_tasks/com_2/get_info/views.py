from rest_framework.response import Response
from rest_framework.views import APIView
from events.models import Events
from events.serializers import EventSerializer


class AllInfoView(APIView):
    def get(self, request):
        one = [{"get_info": {"title": "Title of event", "month": "11"}},
               {"get_info": {"city": "City of event"}}]
        return Response(one)

    def post(self, request):
        event = request.data.get('get_info')
        if 'month' not in event.keys():
            city = event['city']
            event = Events.objects.all()
            answer = []
            serializer = EventSerializer(event, many=True)
            for i in serializer.data:
                if i['city'] == city and i['free_places'] != '0':
                    answer.append(i)
            answer = sorted(answer, key=lambda x: int(x['date'].split('-')[1]) * 30 + int(x['date'].split('-')[2]))
            return Response({"events": answer})
        title = event['title']
        month = event['month']
        event = Events.objects.all()
        answer = []
        serializer = EventSerializer(event, many=True)
        for i in serializer.data:
            if i['title'] == title and (i['date'].split('-')[1] == month or i['periodicity'] == 'каждый день'
                                        or i['periodicity'] == 'каждый месяц'):
                answer.append(i)
        return Response({"events": answer})