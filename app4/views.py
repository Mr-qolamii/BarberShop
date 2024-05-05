from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import generics, ModelViewSet
from rest_framework import status, viewsets
from django_filters.rest_framework import *

from app2.permissions import *
from app3.permissions import IsAdmin
from .permissions import *
from .serializers import *
from .models import *


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(soldout=False).order_by('-id')
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category',)


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdmin,)


class OrderModelViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend,)

    def get_object(self):
        obj = self.queryset.filter(user=self.request.user)
        return obj


class SoldOutListView(generics.ListAPIView):
    queryset = Order.objects.all().order_by('-id')
    serializer_class = SoldOutSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('product', 'user')


class CreateOrderView(generics.CreateAPIView):
        serializer_class = OrderSerializer
        permission_classes = (IsAuthenticated,)

        def create(self, request, pk,*args, **kwargs):
            serializer = self.get_serializer(data={'product': pk, 'user': request.user.id})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GetUserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user).order_by('-id')
