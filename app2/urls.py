from django.urls import reverse, path
from rest_framework.routers import SimpleRouter

from .views import *

app_name = 'posts'

route = SimpleRouter()

route.register("posts", PostViewSet, 'posts')

urlpatterns = []

urlpatterns += route.urls

