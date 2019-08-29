from django.contrib.auth.models import User
from rest_framework import serializers
from bookingApi.models import *


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('pk', 'room_id', 'number_of_people', 'date_start', 'date_end')


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('user', 'room_id', 'room_capacity',)


class BookingSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingSearch
        fields = ('number_of_people', 'date_start', 'date_end')
