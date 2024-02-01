from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .permissions import *
from .serializers import *
from .models import *


class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.filter(is_canceled=False, is_doing=False).order_by('date')
    serializer_class = ReservationsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        reservation = self.get_object()
        reservation.is_canceled = True
        reservation.save()
        return Response({'message': 'Reservation cancelled'}, status=status.HTTP_200_OK)


class AllReservation(ListAPIView):
    queryset = Reservation.objects.all().order_by('date')
    serializer_class = ReservationsForAdminSerializer
    permission_classes = [IsAdmin]
