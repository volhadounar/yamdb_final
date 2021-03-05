from rest_framework import permissions


class IsAdminOrStaff(permissions.BasePermission):
    """Права роли admin или staff"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False


class IsAuthorOrModeratorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Права ролей автора, модератора, пользователя"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_admin or request.user.is_moderator:
            return True
        return obj.author == request.user
