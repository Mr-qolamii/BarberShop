from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('', SignUPView.as_view(), name='signup'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('changepassword/', ChangePasswordView.as_view(), name='setpassword'),
    path('reset/<token>/', ResetPasswordView.as_view(), name='reset_password'),


]


