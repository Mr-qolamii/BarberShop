from django.conf import settings
from rest_framework.permissions import DjangoModelPermissions
import jwt

from .models import User


class NotAuthenticated(DjangoModelPermissions):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False
        else:
            return True


class ExistToken(DjangoModelPermissions):
    def has_permission(self, request, view):
        token = request.get_full_path().split('/')[-2]
        try:
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=settings.SIMPLE_JWT['ALGORITHM'])
            if User.objects.get(pk=payload['user_id']) is not None:
                return True
            else:
                return False
        except:
            return False

