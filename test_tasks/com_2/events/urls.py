from django.urls import path
from .views import EventView

app_name = "events"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('events/', EventView.as_view()),
]