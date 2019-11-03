from django.urls import path
from .views import AllInfoView

app_name = "Information"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('getinfo/', AllInfoView.as_view()),
]