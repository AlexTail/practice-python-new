from django.urls import path
from .views import BuyTicketsView


app_name = "tickets"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('buytickets/', BuyTicketsView.as_view()),
]