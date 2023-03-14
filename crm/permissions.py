from rest_framework.permissions import BasePermission
from crm import models
from rest_framework import permissions as rest_permissions


class ModelPermission(rest_permissions.BasePermission):
    def __init__(self):
        pass

    def _gen_perm(self, action):
        verb = {
            'list': 'view',
            'retrieve': 'view',
            'create': 'add',
            'update': 'change',
            'destroy': 'delete'
        }[action]

        model = self.Meta().model
        module = model.__module__.split('.')[0]
        name = model.__name__.lower()
        return f'{module}.{verb}_{name}'

    def has_permission(self, request, view):
        user = request.user

        rules = [
            rule
            for rule in self.Meta.rules
            if user.is_in_group(rule.group)
        ]

        if len(rules) == 0:
            return False

        actions = []
        for rule in rules:
            actions += rule.actions

        if view.action not in actions:
            return False

        for rule in rules:
            for action in rule.actions:
                perm = self._gen_perm(action)
                if not user.has_perm(perm):
                    return False
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        rules = [
            rule
            for rule in self.Meta.rules
            if user.is_in_group(rule.group)
        ]

        if len(rules) == 0:
            return False

        for rule in rules:
            if rule.object and not rule.object(request, obj):
                return False

        return True


class GroupRule:
    def __init__(self, group_name):
        self.group = group_name
        self.actions = []
        self.object = None

    def for_object(self, obj):
        self.object = obj
        return self

    def read_only(self):
        return self.list().retrieve()

    def crud(self):
        return self.read_only().create().update().destroy()

    def list(self):
        self.actions.append('list')
        return self

    def retrieve(self):
        self.actions.append('retrieve')
        return self

    def create(self):
        self.actions.append('create')
        return self

    def update(self):
        self.actions.append('update')
        return self

    def destroy(self):
        self.actions.append('destroy')
        return self


class UserPermission(ModelPermission):
    class Meta:
        model = models.User
        rules = [
            GroupRule('ManagementTeam').crud()
        ]


def support_customers(request, customer):
    return models.Event.objects.filter(
        support_contact=request.user,
        contract__customer=customer
    ).count() > 0


def sales_customers(request, customer):
    return request.user == customer.sales_contact


def sales_contracts(request, contract):
    return request.user == contract.sales_contact


class CustomerPermission(ModelPermission):
    class Meta:
        model = models.Customer
        rules = [
            GroupRule('ManagementTeam').crud(),

            GroupRule('SalesTeam')
            .for_object(sales_customers)
            .crud(),

            GroupRule('SupportTeam')
            .for_object(support_customers)
            .read_only()
        ]


def support_events(request, event):
    return event.support_contact == request.user


class EventPermission(ModelPermission):
    class Meta:
        model = models.Event
        rules = [
            GroupRule('ManagementTeam').crud(),

            GroupRule('SupportTeam')
            .for_object(support_events)
            .list()
            .retrieve()
            .update(),

            GroupRule('SalesTeam').create()
        ]


class ContractPermission(ModelPermission):
    class Meta:
        model = models.Contract
        rules = [
            GroupRule('ManagementTeam').crud(),

            GroupRule('SalesTeam')
            .for_object(sales_contracts)
            .list()
            .retrieve()
            .update()
        ]