from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to see it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner and obj.owner == request.user