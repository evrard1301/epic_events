from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions as rest_permissions
from crm import permissions
from crm.models import User
from crm.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.CanManageUser]