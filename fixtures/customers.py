import pytest
from crm.models import Customer


@pytest.fixture
def customer(db):
    return Customer.objects.create(first_name='Alice')


@pytest.fixture
def customers(db):
    return {
        'Alice': Customer.objects.create(first_name='Alice', last_name='Altero', email='alice.altero@email.com'),
        'Bob': Customer.objects.create(first_name='Bob', last_name='Bishop', email='bob.bishop@email.com'),
        'Claire': Customer.objects.create(first_name='Claire', last_name='Catty', email='claire.catty@email.com'),
        'Dan': Customer.objects.create(first_name='Dan', last_name='Domann', email='dan.domann@email.com'),
        'Eric': Customer.objects.create(first_name='Eric', last_name='Ecte', email='eric.ecte@email.com'),
        'Fred': Customer.objects.create(first_name='Fred', last_name='Fuero', email='fred.fuero@email.com'),
        'Gary': Customer.objects.create(first_name='Gary', last_name='Gimson', email='sgary.gimson@email.com')
    }
