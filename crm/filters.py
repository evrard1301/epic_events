import django_filters
import django_filters.filters
from django_filters import FilterSet
from crm import models


class CustomerFilter(FilterSet):
    name = django_filters.CharFilter(field_name='last_name')

    class Meta:
        model = models.Customer
        fields = ['name', 'email']


class EventFilter(FilterSet):
    date = django_filters.DateTimeFilter(field_name='event_date')
    name = django_filters.CharFilter(field_name='contract__customer__last_name')
    email = django_filters.CharFilter(field_name='contract__customer__email')

    class Meta:
        model = models.Event
        fields = ['date', 'name', 'email']


class ContractFilter(FilterSet):
    name = django_filters.filters.CharFilter(field_name='customer__last_name')
    email = django_filters.filters.CharFilter(field_name='customer__email')
    date = django_filters.filters.DateTimeFilter(field_name='date_created')

    class Meta:
        model = models.Contract
        fields = ['name', 'email', 'date', 'amount']