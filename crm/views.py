from rest_framework.viewsets import ModelViewSet

from crm.models import (
    User,
    Customer,
    Event,
    Contract
)

from crm.serializers import (
    UserSerializer,
    CustomerSerializer,
    EventSerializer,
    ContractSerializer
)

from crm.permissions import (
    UserPermission,
    CustomerPermission,
    EventPermission,
    ContractPermission
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]


class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [CustomerPermission]

    def get_queryset(self):
        if self.action == 'list' and not self.request.user.is_in_group('ManagementTeam'):
            return Customer.objects.filter(sales_contact=self.request.user.id)
        return Customer.objects.all()


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [EventPermission]

    def get_queryset(self):
        if self.action == 'list' and not self.request.user.is_in_group('ManagementTeam'):
            return Event.objects.filter(support_contact=self.request.user.id)
        return Event.objects.all()


class ContractViewSet(ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [ContractPermission]
    def get_queryset(self):
        if self.action == 'list' and not self.request.user.is_in_group('ManagementTeam'):
            return Contract.objects.filter(sales_contact=self.request.user.id)
        return Contract.objects.all()