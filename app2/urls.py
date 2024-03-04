from rest_framework.routers import SimpleRouter
from django.urls import path

from .views import *

app_name = 'posts'

route = SimpleRouter()

route.register("posts", PostViewSet, 'posts')

urlpatterns = [
    path('posts/<int:pk>/comments/', CommentAPIView.as_view(), name='post_comments'),
    path('posts/<int:pk>/likes/', PostLikeAPIView.as_view(), name='post_likes'),
    path('posts/<int:pk>/views/', PostViewsAPIView.as_view(), name='post_views'),

]

urlpatterns += route.urls
