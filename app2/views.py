from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import generics, ModelViewSet
from rest_framework.response import Response
from django_filters.rest_framework import *
from rest_framework.permissions import *
from rest_framework.filters import *

from app4.permissions import IsOwner
from .models import *
from .serializers import *
from .permissions import *


class PostViewSet(ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Post.objects.all().order_by('-date')
    filter_backends = [SearchFilter]
    search_fields = ["title", "description"]
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data)


class CommentUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsOwner]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class PostLikeAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer

    def create(self, request, *args, **kwargs):
        if Post.objects.filter(id=self.kwargs['pk']).exists():
            if queryset := self.get_queryset().filter(post=self.kwargs['pk'], user=request.user).exists():
                post_like_delete.apply_async(kwargs={"post_id": kwargs['pk'], "user": request.user})
                return Response({"is liked ": False}, status=status.HTTP_200_OK)
            else:
                post_like.apply_async(kwargs={"post_id": kwargs['pk'], "user": request.user})
                return Response({"is liked ": True}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "post not exist"}, status=status.HTTP_404_NOT_FOUND)


