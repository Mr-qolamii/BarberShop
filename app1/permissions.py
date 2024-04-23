from rest_framework.permissions import DjangoModelPermissions

from .models import User

class NotAuthenticated(DjangoModelPermissions):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False
        else:
            return True

class ExistToken(DjangoModelPermissions):
    def has_permission(self, request, view):
        pass
