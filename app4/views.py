from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import generics
from rest_framework import status, viewsets
from django_filters.rest_framework import *

from app2.permissions import *
from app3.permissions import *
from .permissions import *
from .serializers import *
from .models import *


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('category', )
    search_fields = ('description',)


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdmin,)


class SoldOutListView(generics.ListAPIView):
    queryset = Order.objects.filter(is_done=True).order_by('-id')
    serializer_class = SoldOutSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('product', 'user')


class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GetUserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user).order_by('-id')
        return queryset


class UpdateOrderView(generics.DestroyAPIView, generics.RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user).order_by('-id')
        return queryset


class RetrieveOrderView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user).order_by('-id')
        return queryset
