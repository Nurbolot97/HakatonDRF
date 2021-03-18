from rest_framework.permissions import BasePermission


class IsCategoryOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user == request.user.is_staff


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active