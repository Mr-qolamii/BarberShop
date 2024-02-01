from rest_framework.viewsets import generics, ModelViewSet
from rest_framework.response import Response
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


class CommentAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(post=self.kwargs['pk'])
        serializer = self.get_serializer(queryset, menu=True)
        return Response(data=serializer.data)


class PostLike(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PostLike.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(post=self.kwargs['pk'])
        if queryset.filter(user=self.kwargs['user']).exists():
            return Response({"post likes count is": queryset.count(), "is liked": True})
        else:
            return Response({"post likes count is": queryset.count(), "is liked": False})

    def create(self, request, *args, **kwargs):
        kwargs['user'] = request.user
        kwargs['post'] = kwargs['pk']
        if not PostLike.objects.filter(post=self.kwargs['pk'], user=kwargs['user']).exists():
            post_like.apply_async(kwargs=kwargs)
        return Response({"detail": True})
