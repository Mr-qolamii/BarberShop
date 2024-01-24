from rest_framework.routers import SimpleRouter

from .views import *

app_name = 'posts'

route = SimpleRouter()

route.register("posts", PostViewSet, 'posts')
route.register("comments", CommentViewSet, 'comments')

urlpatterns = []

urlpatterns += route.urls

