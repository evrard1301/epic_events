from rest_framework.permissions import BasePermission
from crm import models


class HasPermission(BasePermission):
    def __init__(self, perm):
        self.perm = perm

    def has_permission(self, request, view):
        return request.user.has_perm(self.perm)


class CanManageUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_in_group('ManagementTeam')


class CanManageCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, customer):
        if request.user.is_in_group('ManagementTeam'):
            return True

        if request.user.is_in_group('SalesTeam'):
            return request.user == customer.sales_contact

        if request.user.is_in_group('SupportTeam'):
            return customer in [
                event.contract.customer
                for event in models.Event.objects.all()
                if event.support_contact == request.user
            ]

        return False
