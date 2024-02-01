from rest_framework.viewsets import generics, ModelViewSet
from django_filters.rest_framework import *
from rest_framework.permissions import *
from rest_framework.filters import *

from .models import *
from .serializers import *
from .permissions import *


class PostViewSet(ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Post.objects.all().order_by('-date')
    filter_backends = [SearchFilter]
    search_fields = ["title", "description"]
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        if not PostViews.objects.filter(user=request.user, post=self.kwargs['pk']).exists():
            post_view.apply_async(kwargs={"post": self.kwargs['pk'], "user": self.request.user})
        return super().retrieve(request, *args, **kwargs)


class CommentViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Comment.objects.all().order_by('-date')
    serializer_class = CommentSerializer


