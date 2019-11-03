from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Events
from .serializers import EventSerializer


class EventView(APIView):
    def get(self, request):
        event = Events.objects.all()
        serializer = EventSerializer(event, many=True)
        events = serializer.data
        events = sorted(events, key=lambda x: x["city"])
        nn = {
                "title": "Title of event",
                "date": "Date of event",
                "city": "City of event",
                "free_places": "free_places",
                "price": "price",
                "periodicity": "каждый день/каждый месяц/каждый год/разово"
            }
        return Response([{"events": nn}, {"events": events}])

    def post(self, request):
        event = request.data.get('events')
        serializer = EventSerializer(data=event)
        if serializer.is_valid(raise_exception=True):
            event_saved = serializer.save()
        return Response({"success": "Event '{}' created successfully".format(event_saved.title)})