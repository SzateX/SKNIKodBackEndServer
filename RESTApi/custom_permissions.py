from rest_framework import permissions


class MyPermission(permissions.BasePermission):
    message = "I don't give it for you."

    def has_permission(self, request, view):
        pass

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

