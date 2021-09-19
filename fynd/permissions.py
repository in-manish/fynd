from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser:
            return True
        return False


class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_staff:
            return True
        return False
