from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """Права администратора."""
    def has_permission(self, request, view):
        return request.user.is_admin
