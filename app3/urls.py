from rest_framework.routers import SimpleRouter

from .views import *

route = SimpleRouter()

route.register("reservation", ReservationViewSet, "reservation")

urlpatterns = []

urlpatterns += route.urls
