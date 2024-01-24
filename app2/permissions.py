from rest_framework.permissions import BasePermission


class IsAdminUserOrReadOnly(BasePermission):
    SAFE_METHODS = ["GET", "HEADER",  "OPTION"]

    def has_object_permission(self, request, view, obj):
        return bool(request.method in self.SAFE_METHODS or request.user and request.user.is_superuser)
