from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions as rest_permissions
from crm import permissions
from crm.models import User, Customer
from crm.serializers import UserSerializer, CustomerSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.CanManageUser]


class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        if self.action == 'list' and not self.request.user.is_in_group('ManagementTeam'):
            return Customer.objects.filter(sales_contact=self.request.user.id)
        return Customer.objects.all()

    def get_permissions(self):
        perms = {
            'create': [permissions.HasPermission('crm.add_customer')],
            'list': [permissions.CanManageCustomer()],
            'retrieve': [permissions.CanManageCustomer()],
            'update': [permissions.CanManageCustomer()],
            'destroy': [permissions.CanManageCustomer()]
        }

        return perms[self.action] + [
            rest_permissions.IsAuthenticated()
        ]