from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit/delete/read it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username
