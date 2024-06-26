from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsModerator(BasePermission):
    """Проверка прав модератора"""
    def has_permission(self, request, view):
        return request.user.role == UserRoles.MODERATOR


class IsOwner(BasePermission):
    """Проверка владельца"""
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
