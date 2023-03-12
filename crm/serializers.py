from rest_framework.serializers import ModelSerializer
from crm.models import User, Customer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name'
        ]
        extra_kwargs = {
            'password': {"read_only': True"}
        }


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'