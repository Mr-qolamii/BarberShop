from rest_framework import status
from rest_framework.views import APIView
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
            post_view.apply_async(kwargs={"post_id": self.kwargs['pk'], "user": self.request.user})
        return super().retrieve(request, *args, **kwargs)


class CommentAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(post=self.kwargs['pk'])
        serializer = self.get_serializer(queryset, menu=True)
        return Response(data=serializer.data)


class PostLikeAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(post=self.kwargs['pk'])
        if queryset.filter(user=request.user).exists():
            return Response({"post likes count is": queryset.filter(post=self.kwargs['pk']).count(), "is liked": True})
        else:
            return Response({"post likes count is": queryset.filter(post=self.kwargs['pk']).count(), "is liked": False})

    def create(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(post=self.kwargs['pk'])
        if queryset.filter(user=request.user).exists():
            post_like_delete.apply_async(kwargs={"post_id": kwargs['pk'], "user": request.user})
            return Response({"is liked ": False}, status=status.HTTP_200_OK)
        else:
            post_like.apply_async(kwargs={"post_id": kwargs['pk'], "user": request.user})
            return Response({"is liked ": True}, status=status.HTTP_200_OK)


class PostViewsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        views_cont = PostViews.objects.filter(post=self.kwargs['pk']).count()
        return Response({"views": views_cont})

