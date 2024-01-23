from rest_framework.viewsets import generics, ModelViewSet
from django_filters.rest_framework import *
from rest_framework.permissions import *
from rest_framework.filters import *

from .models import *
from .serializers import *


class PostViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Post.objects.all().order_by('-date')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["location", "user", "title"]
    ordering_fields = ["price"]
    filterset_fields = {"location": ["exact", "in"], "price": ["lt", "gt"]}
    serializer_class = PostSerializer
