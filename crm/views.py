from rest_framework.viewsets import ModelViewSet
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

    def get_queryset(self):
        customers = Customer.objects.all()
        if self.action == 'list':
            name_filter = self.request.GET.get('name', None)
            customers = customers.filter(last_name=name_filter) if name_filter is not None else customers

            email_filter = self.request.GET.get('email', None)
            customers = customers.filter(email=email_filter) if email_filter is not None else customers

        return customers


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [EventPermission]

    def get_queryset(self):
        events = Event.objects.all()

        if self.action == 'list':
            name_filter = self.request.GET.get('name', None)
            events = events.filter(contract__customer__last_name=name_filter) if name_filter is not None else events

            email_filter = self.request.GET.get('email', None)
            events = events.filter(contract__customer__email=email_filter) if email_filter is not None else events

            date_filter = self.request.GET.get('date', None)
            date_components = date_filter.split('_') if date_filter is not None else None

            events = events.filter(
                event_date__day=date_components[0],
                event_date__month = date_components[1],
                event_date__year = date_components[2]
            ) if date_components is not None else events

        return events


class ContractViewSet(ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [ContractPermission]

    def get_queryset(self):
        contracts = Contract.objects.all()

        if self.action == 'list':
            name_filter = self.request.GET.get('name', None)
            contracts = contracts if name_filter is None else contracts.filter(customer__last_name=name_filter)

            email_filter = self.request.GET.get('email', None)
            contracts = contracts if email_filter is None else contracts.filter(customer__email=email_filter)

            date_filter = self.request.GET.get('date', None)
            mydate = date_filter.split('_') if date_filter is not None else None
            contracts = contracts if mydate is None else contracts.filter(date_created__day=int(mydate[0]),
                                                                          date_created__month=int(mydate[1]),
                                                                          date_created__year=int(mydate[2]))

            amount_filter = self.request.GET.get('amount', None)
            contracts = contracts if amount_filter is None else contracts.filter(amount=amount_filter)

        if self.action == 'list' and not self.request.user.is_in_group('ManagementTeam'):
            return contracts.filter(sales_contact=self.request.user.id)

        return contracts
