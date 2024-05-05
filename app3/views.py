from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status, generics

from .permissions import *
from .serializers import *
from .models import *


class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.filter(is_canceled=False, is_done=False).order_by('date')
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
    filter_backends = [DjangoFilterBackend]
    fields = ["is_canceled", "is_done"]


class GetUserReservation(generics.RetrieveAPIView):
    serializer_class = ReservationsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = Reservation.objects.get(user=self.request.user)
        return obj


