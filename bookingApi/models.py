from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Room(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room_id = models.CharField(max_length=80, primary_key=True, serialize=True)
    room_capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.room_id


class Booking(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    number_of_people = models.IntegerField()
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()


class BookingSearch(models.Model):
    number_of_people = models.IntegerField()
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
