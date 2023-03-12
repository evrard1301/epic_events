from rest_framework.permissions import BasePermission


class CanManageUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_in_group('ManagementTeam')

