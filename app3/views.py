from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from .models import *
from .serializers import *


class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.all().order_by('date')
    serializer_class = ReservationsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
