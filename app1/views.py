from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.viewsets import generics
from django.utils import timezone
from django.urls import reverse

from .serializers import *
from .permissions import *
from .models import *
from .tasks import *


class SignUPAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [NotAuthenticated]


class RegisterAPIView(generics.GenericAPIView):
    permission_classes = [NotAuthenticated]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request, username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        if user is not None:
            login(request, user)
            device = {
                "user": request.user, "device_name": request.META.get('HTTP_USER_AGENT'),
                "login_time": timezone.now(),
                "is_active": True
            }
            save_device.delay(**device)
            return Response(status=status.HTTP_200_OK)
        return Response({'detail': "username or password is incorrect"}, status=status.HTTP_401_UNAUTHORIZED)


class LogOutAPIView(generics.GenericAPIView):
    """ Logout view """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        delete_device.delay(device_name=request.META.get('HTTP_USER_AGENT'), user_id=request.user.id)
        logout(request)
        return Response({'detail': 'logout success'}, status=status.HTTP_200_OK)


class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = UserSetPasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.check_password(raw_password=serializer.validated_data['password']):
            serializer.update(request.user, serializer.validated_data)
            return Response({'detail': 'password updated'}, status=status.HTTP_200_OK)
        else:
            raise serializers.ValidationError({'password': 'old password is false'})

    def get_object(self):
        return self.request.user


class SendLinkForResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = SendSMSForResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_sms.delay(tell=serializer.validated_data['tell'], token=serializer.validated_data['token'])
        return Response({'detail': 'The link has been sent to you'})


class ResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [ExistToken]

    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=settings.SIMPLE_JWT['ALGORITHM'])
        user = User.objects.get(pk=payload.get('user_id'))
        user.set_password(serializer.validated_data['password_now'])
        user.save()
        return Response({'detail': 'set password success'}, status=status.HTTP_200_OK)


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = Profile.objects.get(pk=self.request.user.pk)
        return obj

