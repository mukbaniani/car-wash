from rest_framework.permissions import BasePermission, SAFE_METHODS

class CanDelete(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsWasher(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_washer is True