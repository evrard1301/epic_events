import pytest
from crm.models import User, Customer, Contract, Event
from django.contrib.auth.models import Group
from django.utils import timezone


@pytest.fixture
def noteam_employee(db):
    user = User.objects.create(
        first_name='Stan',
        last_name='Serion',
        email='stan.serion@email.com',
        username='sserion'
    )

    return user


@pytest.fixture
def management_employee(db):
    user = User.objects.create(
        first_name='Eric',
        last_name='Elliot',
        email='eric.elliot@email.com',
        username='eelliot'
    )

    group = Group.objects.get(name='ManagementTeam')
    user.groups.add(group)
    user.save()

    return user


@pytest.fixture
def sales_employee(db):
    user = User.objects.create(
        first_name='Theo',
        last_name='Tallio',
        email='theo.tallio@email.com',
        username='ttallio'
    )

    group = Group.objects.get(name='SalesTeam')
    user.groups.add(group)
    user.save()

    return user


@pytest.fixture
def sales_employee__customer(sales_employee, customer):
    customer.sales_contact=sales_employee
    customer.save()
    return sales_employee


@pytest.fixture
def support_employee(db):
    user = User.objects.create(
        first_name='Patt',
        last_name='Pototo',
        email='patt.pototo@email.com',
        username='ppototo'
    )

    group = Group.objects.get(name='SupportTeam')
    user.groups.add(group)
    user.save()

    return user


@pytest.fixture
def support_employee__customer(support_employee, customer):

    contract = Contract.objects.create(
        amount=34.5,
        customer=customer,
        payment_due=timezone.now(),
    )

    Event.objects.create(
        support_contact=support_employee,
        contract=contract,
        attendee=4,
        event_date=timezone.now(),
    )

    return support_employee
