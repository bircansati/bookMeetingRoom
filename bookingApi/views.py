from bookingApi.models import Booking, Room
from bookingApi.serializers import BookingSerializer, RoomSerializer, BookingSearchSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.db.models import Avg, Max, Min, Sum, Q
from django.core import serializers
import datetime


class AvailableRooms(APIView):

    def post(self, request, format=None):
        serializer = BookingSearchSerializer(data=request.data)
        if serializer.is_valid():
            entries1 = Room.objects.filter(
                Q(booking__date_start__gte=serializer.data.get('date_start')) &
                Q(booking__date_end__lte=serializer.data.get('date_end'))
            )
            entries2 = Room.objects.exclude(room_id__in=entries1)
            if not entries2:
                Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                entries3 = entries2.filter(room_capacity__gte=serializer.data.get('number_of_people'))
                min_value = (entries3.aggregate(Min('room_capacity')))
                entries = entries3.filter(room_capacity=min_value.get('room_capacity__min'))
                room_id = entries.values()[0].get('room_id')

                content = {
                    'room_id': entries.values()[0].get('room_id'),
                    'number_of_people': serializer.data.get('number_of_people'),
                    'date_start': serializer.data.get('date_start'),
                    'date_end': serializer.data.get('date_end'),
                }

                booking_serializer = BookingSerializer(data=content)
                if booking_serializer.is_valid():
                    return Response(booking_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookRoom(APIView):
    def post(self, request, format=None):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
