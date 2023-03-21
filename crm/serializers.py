from rest_framework.serializers import ModelSerializer
from crm.models import (
    User,
    Customer,
    Event,
    Contract
)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        ]
        extra_kwargs = {
            'password': {"write_only": True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class ContractSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'
