from django.db import models


class Events(models.Model):
    title = models.CharField(max_length=120)
    date = models.DateField()
    city = models.CharField(max_length=120)
    free_places = models.CharField(max_length=120)
    price = models.CharField(max_length=120)
    periodicity = models.CharField(max_length=120)

    def __str__(self):
        return self.title