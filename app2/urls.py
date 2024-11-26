from rest_framework.routers import SimpleRouter
from django.urls import path

from .views import *

app_name = 'posts'

route = SimpleRouter()

route.register("posts", PostViewSet, 'posts')

urlpatterns = [
    path('posts/<int:pk>/comments/', CommentAPIView.as_view(), name='post_comments'),
    path('posts/<int:pk>/like/', PostLikeAPIView.as_view(), name='post_likes'),
    path('comments/<int:pk>/', CommentUpdateAPIView.as_view(), name='comment_update'),

]

urlpatterns += route.urls
