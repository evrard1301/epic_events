from pytest_bdd import scenarios
from pytest_bdd import given, when, then, parsers
from fixtures import *

pytestmark = pytest.mark.django_db

scenarios('management.feature')


@pytest.fixture(scope='module')
def ctx():
    return {
        'username': '',
        'password': ''
    }


@given(parsers.parse('A new member of the {team}.'))
def new_member_to_add(ctx, team):
    ctx['username'] = 'bob'
    ctx['password'] = 'bobpassword'
    ctx['group'] = team


@when('I create its user account.')
def create_account(client, management_employee, ctx):
    client.force_login(management_employee)

    res = client.post(reverse_lazy('crm:users-list'), {
        'username': ctx['username'],
        'password': ctx['password']
    })

    pk = res.data['id']
    ctx['id'] = pk

    res = client.post(reverse_lazy('crm:users-grant', kwargs={
        'pk': pk
    }), {
        'group': ctx['group']
    })

    assert status.HTTP_200_OK == res.status_code


@when(parsers.parse('I change its group to {team}.'))
def change_group(client, team, ctx, management_employee):
    client.force_login(management_employee)
    print(team)
    res = client.post(reverse_lazy('crm:users-grant', kwargs={
        'pk': ctx['id']
    }), {
        'group': team
    })

    assert status.HTTP_200_OK == res.status_code


@then('The user can log in the CRM.')
def can_log_in(client, ctx):
    res = client.post(reverse_lazy('crm:login'), {
        'username': ctx['username'],
        'password': ctx['password']
    })

    assert status.HTTP_200_OK == res.status_code


@then(parsers.parse('The user is in the group "{team}".'))
def in_group(ctx, team):
    user = User.objects.get(username=ctx['username'])
    assert user.is_in_group(team)
    assert 1 == len(user.groups.all())
