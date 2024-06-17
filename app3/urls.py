from rest_framework.routers import SimpleRouter
from django.urls import path

from .views import *

urlpatterns = [
    path('allreservations/', AllReservation.as_view(), name="all_reservations"),
    path('myreservations/', GetUserReservation.as_view(), name="user_reservations"),
    path('reservations/', ReservationAPIView.as_view(), name="reservations"),


    ]
