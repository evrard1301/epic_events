from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from crm import filters
import datetime


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
    queryset = Customer.objects.all()
    filterset_class = filters.CustomerFilter


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [EventPermission]
    filterset_class = filters.EventFilter
    queryset=Event.objects.all()


class ContractViewSet(ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [ContractPermission]
    queryset = Contract.objects.all()
    filterset_class = filters.ContractFilter