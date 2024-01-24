from rest_framework.permissions import BasePermission

SAFE_METHODS = ["GET", "HEADER",  "OPTION"]


class IsAdminUserOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(request.method in SAFE_METHODS or request.user and request.user.is_superuser)


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.method in SAFE_METHODS or request.user == obj.user)