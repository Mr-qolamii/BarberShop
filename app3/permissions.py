from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    safe_methods = ['get', 'HEAD', 'OPTIONS']

    def has_object_permission(self, request, view, obj):
        return bool(request.method in self.safe_methods or obj.user == request.user)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)