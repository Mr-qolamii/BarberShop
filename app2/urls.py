from rest_framework.routers import SimpleRouter
from django.urls import path

from .views import *

app_name = 'posts'

route = SimpleRouter()

route.register("posts", PostViewSet, 'posts')

urlpatterns = [
    path('posts/<int:pk>/comments/', CommentAPIView.as_view(), name='post_comments')

]

urlpatterns += route.urls
