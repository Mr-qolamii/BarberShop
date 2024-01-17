from rest_framework import status, permissions
from rest_framework.viewsets import generics
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout

from Celery.tasks import *
from .models import *
from .serializers import *
from .permissions import *


class SignUPView(generics.GenericAPIView):
    serializer_class = UserSerializer

    permission_classes = [NotAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'User Created'}, status=status.HTTP_201_CREATED)
 

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    permission_classes = [NotAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(self.request, username=serializer.validated_data['username'],
                                            password=serializer.validated_data['password'])
        if user is not None:
            login(request, user)
            return Response({'detail': 'login success'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Login is not successful'}, status=status.HTTP_400_BAD_REQUEST)


class LogOutView(generics.GenericAPIView):
    """ Logout view """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response({'detail': 'logout success'}, status=status.HTTP_200_OK)


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = UserSetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.request.user.check_password(serializer.validated_data['password']):
            self.request.user.set_password(serializer.validated_data['password_now'])
            login(request, self.request.user)
            return Response({'detail': 'login success'}, status=status.HTTP_200_OK)
        raise ValidationError({'detail': 'not login success'})


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = RestPasswordSerializer

    def post(self, request):
        self.request.user.check_password()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['password'] == serializer.validated_data['password_2']:
            self.request.user.set_password(serializer.validated_data['password'])
            return Response({'detail': 'set password success'}, status=status.HTTP_200_OK)

        raise ValidationError({'detail': 'password not match'})
