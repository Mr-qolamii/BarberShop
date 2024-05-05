from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

app_name = 'account'

urlpatterns = [
    path('', SignUPAPIView.as_view(), name='signup'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('logout/', LogOutAPIView.as_view(), name='logout'),
    path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('changepassword/', ChangePasswordAPIView.as_view(), name='setpassword'),
    path('reset/<token>/', ResetPasswordAPIView.as_view(), name='reset_password'),
    path('changeprofile/', UpdateProfileAPIView.as_view(), name='change_profile'),
    path('forgetpassword/', SendLinkForResetPasswordAPIView.as_view(), name='send_reset_password_link'),
]


