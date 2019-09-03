from rest_framework.routers import DefaultRouter

from bookingApi import views
from bookingApi.views import *
from django.urls import path, include

app_name = 'bookingApi'
router = DefaultRouter()
router.register(r'booking', views.BookingViewSet)
router.register(r'room', views.RoomViewSet, base_name='room')
urlpatterns = [

    path('availablerooms/', AvailableRooms.as_view(), name="availablerooms"),
    path('bookroom/', BookRoom.as_view(), name="bookroom"),
    path('', include(router.urls))
]
