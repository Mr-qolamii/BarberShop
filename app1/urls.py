from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', SignUPView.as_view(), name='signup'),
    path('logout/', LogOutView.as_view(), name='logout'),

]


