from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions
from rest_framework.viewsets import generics
from rest_framework.response import Response
from django.utils import timezone

from .tasks import *
from .serializers import *
from .permissions import *
from .models import *


class SignUPAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [NotAuthenticated]


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    permission_classes = [NotAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(self.request, username=serializer.validated_data['username'],
                            password=serializer.validated_data['password'])
        if user is not None:
            login(request, user)
            device = {"user": request.user, "device_name": request.META.get('HTTP_USER_AGENT'),
                      "login_time": timezone.now(), "is_active": True}
            Device.objects.create(**device)
            return Response({'detail': 'login success'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Login is not successful'}, status=status.HTTP_400_BAD_REQUEST)


class LogOutAPIView(generics.GenericAPIView):
    """ Logout view """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        Device.objects.get(device_name=request.META.get('HTTP_USER_AGENT'), user_id=request.user.id).delete()
        logout(request)
        return Response({'detail': 'logout success'}, status=status.HTTP_200_OK)


class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = UserSetPasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(id=request.user.id)
        if user.check_password(serializer.validated_data['password_old']):
            user.set_password(serializer.validated_data['password_now'])
            user.save()
            return Response({'detail': 'password set success'}, status=status.HTTP_200_OK)
        raise ValidationError({'detail': 'password is false'})


class SendLinkForResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = SendSMSForResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_sms.delay(tell=serializer.validated_data['tell'], msg=User.objects.get(tell=serializer.validated_data['tell']).get_session_auth_hash())
        return Response({'detail': 'The link has been sent to you'})


class ResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        self.request.user.check_password()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['password'] == serializer.validated_data['password_2']:
            self.request.user.set_password(serializer.validated_data['password'])
            return Response({'detail': 'set password success'}, status=status.HTTP_200_OK)

        raise ValidationError({'detail': 'password not match'})


class UpdateProfileAPIView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = Profile.objects.get(pk=self.request.user.pk)
        return obj
