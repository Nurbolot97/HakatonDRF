from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAdminUser


class IsCommentOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user == IsAdminUser
        
