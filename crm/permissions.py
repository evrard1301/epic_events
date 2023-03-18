from rest_framework.permissions import BasePermission
from crm import models
from rest_framework import permissions as rest_permissions


class Perm:
    def __init__(self, action, scope):
        self.action = action
        self.scope = scope


class ModelPermission(rest_permissions.BasePermission):
    def __init__(self):
        pass

    def _gen_perm(self, action):
        verb = {
            'list': 'view',
            'retrieve': 'view',
            'create': 'add',
            'update': 'change',
            'destroy': 'delete',
            'grant': 'grant',
            'sign': 'sign'
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
            actions += [p.action for p in rule.actions]

        if view.action not in actions:
            return False

        for rule in rules:
            for permission in rule.actions:
                perm = self._gen_perm(permission.action)
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
            for perm in rule.actions:
                if perm.action != view.action:
                    continue

                if perm.scope and not perm.scope(request, obj):
                    return False

        return True


class GroupRule:
    def __init__(self, group_name):
        self.group = group_name
        self.actions = []

    def for_object(self, obj):
        return self

    def read_only(self):
        return self.list().retrieve()

    def crud(self, scope=None):
        return self.read_only().alter(scope)

    def alter(self, scope=None):
        return self.create(scope).update(scope).destroy(scope)

    def list(self, scope=None):
        self.actions.append(Perm('list', scope))
        return self

    def retrieve(self, scope=None):
        self.actions.append(Perm('retrieve', scope))
        return self

    def create(self, scope=None):
        self.actions.append(Perm('create', scope))
        return self

    def update(self, scope=None):
        self.actions.append(Perm('update', scope))
        return self

    def destroy(self, scope=None):
        self.actions.append(Perm('destroy', scope))
        return self

    def action(self, name, scope=None):
        self.actions.append(Perm(name, scope))
        return self


class UserPermission(ModelPermission):
    class Meta:
        model = models.User
        rules = [
            GroupRule('ManagementTeam').crud().action('grant')
        ]


def support_customers(request, customer):
    return models.Event.objects.filter(
        support_contact=request.user,
        contract__customer=customer
    ).count() > 0


def sales_customers(request, customer):
    return request.user == customer.sales_contact


def sales_contracts(request, contract):
    return request.user == contract.customer.sales_contact


def sales_events(request, event):
    return event.contract.customer.sales_contact == request.user


class CustomerPermission(ModelPermission):
    class Meta:
        model = models.Customer
        rules = [
            GroupRule('ManagementTeam').crud(),

            GroupRule('SalesTeam')
            .read_only()
            .alter(sales_customers),

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

            GroupRule('SalesTeam')
            .crud(sales_events),

            GroupRule('SupportTeam')
            .read_only()
            .update(support_events)
            .destroy(support_events)
        ]


class ContractPermission(ModelPermission):
    class Meta:
        model = models.Contract
        rules = [
            GroupRule('ManagementTeam').crud().action('sign'),

            GroupRule('SalesTeam').crud(sales_contracts)
                                  .action('sign', sales_contracts),

            GroupRule('SupportTeam').read_only()
        ]