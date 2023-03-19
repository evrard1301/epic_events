from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from crm import filters


from crm.models import (
    User,
    Customer,
    Event,
    Contract,
    ContractStatus
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

    @action(detail=True, methods=['post'], name='grant')
    def grant(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.groups.clear()
        grp = Group.objects.get(name=request.POST.get('group'))
        grp.user_set.add(user)
        grp.save()
        user.save()
        s = UserSerializer(user)
        return Response(s.data)


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

    @action(detail=True, methods=['post'], name='sign')
    def sign(self, request, pk):
        contract = get_object_or_404(Contract, pk=pk)
        self.check_object_permissions(request, contract)

        contract.status = ContractStatus.objects.create(
            name='signed'
        )

        contract.save()

        return Response()