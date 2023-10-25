from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    SAFE_METHODS = ["GET"]

    def has_object_permission(self, request, view, obj):
        if not obj.created_by.id == request.user.id:
            return request.method in self.SAFE_METHODS
        else:
            return True
