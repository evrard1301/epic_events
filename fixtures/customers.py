import pytest
from crm.models import Customer


@pytest.fixture
def customer(db, sales_employee2):
    return Customer.objects.create(
        first_name='Alice',
        sales_contact=sales_employee2
    )


@pytest.fixture
def customers(db, sales_employee):
    return {
        'Alice': Customer.objects.create(
            first_name='Alice',
            last_name='Altero',
            email='alice.altero@email.com',
            sales_contact=sales_employee
        ),
        'Bob': Customer.objects.create(
            first_name='Bob',
            last_name='Bishop', email='bob.bishop@email.com',
            sales_contact=sales_employee
        ),
        'Claire': Customer.objects.create(
            first_name='Claire',
            last_name='Catty', email='claire.catty@email.com',
            sales_contact=sales_employee
        ),
        'Dan': Customer.objects.create(
            first_name='Dan',
            last_name='Domann', email='dan.domann@email.com',
            sales_contact=sales_employee
        ),
        'Eric': Customer.objects.create(
            first_name='Eric',
            last_name='Ecte', email='eric.ecte@email.com',
            sales_contact=sales_employee
        ),
        'Fred': Customer.objects.create(
            first_name='Fred',
            last_name='Fuero', email='fred.fuero@email.com',
            sales_contact=sales_employee
        ),
        'Gary': Customer.objects.create(
            first_name='Gary',
            last_name='Gimson', email='sgary.gimson@email.com',
            sales_contact=sales_employee
        )
    }
