from rest_framework import permissions


class MyPermission(permissions.BasePermission):
    message = "I don't give it for you."

    def has_permission(self, request, view):
        pass

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )


class IsOwnerOrAdminForUserViewOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_staff or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_staff or request.user.id == obj.id)


class IsOwnerOrAdminForCommentViewOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_staff or request.user.id == obj.user.id)
