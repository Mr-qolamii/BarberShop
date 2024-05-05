from rest_framework.routers import SimpleRouter
from django.urls import path

from .views import *

route = SimpleRouter()

route.register("reservations", ReservationViewSet, "reservations")

urlpatterns = [
    path('allreservations/', AllReservation.as_view(), name="all_reservations"),
    path('userreservations/', GetUserReservation.as_view(), name="user_reservations"),

    ]

urlpatterns += route.urls
