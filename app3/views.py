from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.http import Http404

from .permissions import *
from .serializers import *
from .models import *


class ReservationAPIView(generics.ListCreateAPIView):
    queryset = Reservation.objects.filter(is_canceled=False, is_done=False).order_by('date')
    serializer_class = ReservationsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AllReservation(ListAPIView):
    queryset = Reservation.objects.all().order_by('date')
    serializer_class = ReservationsForAdminSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['is_canceled', 'is_done']


class GetUserReservation(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = ReservationsSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        instance.is_canceled = True
        instance.save()

    def get_object(self):
        try:
            obj = Reservation.objects.get(user=self.request.user, is_canceled=False, is_done=False)
        except Reservation.DoesNotExist:
            raise Http404
        return obj
