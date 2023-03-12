import pytest
from crm.models import User
from django.contrib.auth.models import Group

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
