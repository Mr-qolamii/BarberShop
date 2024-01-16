from rest_framework import status, permissions
from rest_framework.viewsets import generics
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout

from Celery.tasks import *
from .models import *
from .serializers import *


class SignUPView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'User Created'}, status=status.HTTP_201_CREATED)
 

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(serializer.validated_data['username'], serializer.validated_data['password'])
        if user is not None:
            login(request, user)
            return Response({'detail': 'login success'}, status=status.HTTP_200_OK)
        return Response({'detail': 'not login success'}, status=status.HTTP_400_BAD_REQUEST)


class LogOutView(generics.GenericAPIView):
    """ Logout view """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response({'detail': 'logout success'}, status=status.HTTP_200_OK)
