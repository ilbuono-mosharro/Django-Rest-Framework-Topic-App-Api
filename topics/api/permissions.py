from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerUser(BasePermission):
    """
    Allows access only to Owner users.
    """

    def has_object_permission(self, request, view, obj):
        return bool(obj.starter == request.user)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS