from rest_framework.permissions import DjangoModelPermissions


class NotAuthenticated(DjangoModelPermissions):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False
        return True
