from rest_framework import serializers
from .models import Events


class EventSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    date = serializers.DateField()
    city = serializers.CharField(max_length=120)
    free_places = serializers.CharField(max_length=120)
    price = serializers.CharField(max_length=120)
    periodicity = serializers.CharField(max_length=120)

    def create(self, validated_data):
        return Events.objects.create(**validated_data)