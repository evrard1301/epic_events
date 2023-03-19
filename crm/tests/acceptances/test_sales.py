from pytest_bdd import given, when, then
from pytest_bdd import scenarios, parsers
from fixtures import *

pytestmark = pytest.mark.django_db

scenarios('sales.feature')


@pytest.fixture(scope="module", autouse=True)
def ctx():
    class Context:
        name = None
        id = None
        contract_id = None

    return Context()


@given(parsers.parse('A customer {name}.'))
def given_customer(name, sales_employee):
    c = Customer.objects.create(
        first_name=name,
        sales_contact=sales_employee
    )

    ctx.id = c.id


@when(parsers.parse('I change customer phone to "{value}".'))
def change_customer(client, value, sales_employee):
    client.force_login(sales_employee)

    res = client.put(reverse_lazy('crm:customers-detail', kwargs={
        'pk': ctx.id
    }), {
        'first_name': 'Dan',
        'last_name': 'Nad',
        'phone': value,
        'mobile': value,
        'email': 'dan@email.com',
        'company': 'DanInc',
        'sales_contact': sales_employee.id
    })

    assert status.HTTP_200_OK == res.status_code


@then(parsers.parse('The new phone is "{value}".'))
def attribute_is(value):
    assert value == Customer.objects.get(pk=ctx.id).phone


@given(parsers.parse('A prospect {name}.'))
def given_a_prospect(name):
    ctx.name = name


@when('I add the prospect.')
def add_prospect(client, sales_employee):
    client.force_login(sales_employee)

    res = client.post(reverse_lazy('crm:customers-list'), {
        'first_name': ctx.name,
        'last_name': 'NotImportant',
        'email': 'some@email.com',
        'company': 'my company',
        'phone': '000-000-000',
        'mobile': '000-000-000',
        'sales_contact': sales_employee.id
    })

    ctx.id = res.data['id']

    assert status.HTTP_201_CREATED == res.status_code


@when(parsers.parse('I create a contract.'))
def create_contract(client, management_employee):
    client.force_login(management_employee)

    res = client.post(reverse_lazy('crm:contracts-list'), {
        'amount': 7.2,
        'customer': ctx.id,
        'payment_due': timezone.now()
    })

    ctx.contract_id = res.data['id']
    assert status.HTTP_201_CREATED == res.status_code


@when(parsers.parse('{name} sign the contract.'))
def sign_contract(client, management_employee):
    client.force_login(management_employee)

    res = client.post(reverse_lazy('crm:contracts-sign', kwargs={
        'pk': ctx.contract_id
    }))

    assert status.HTTP_200_OK == res.status_code


@then(parsers.parse('{name} has an account.'))
def has_account(name):
    assert Customer.objects.filter(first_name=name).count() == 1


@then(parsers.parse('{name} is a customer.'))
def is_customer(name):
    assert Contract.objects.filter(
        customer__first_name=name,
        status__name="signed"
    ).count() > 0


@then(parsers.parse('{name} is a prospect.'))
def is_prospect(name):
    assert Contract.objects.filter(
        customer__first_name=name,
        status__name="signed"
    ).count() == 0


@then(parsers.parse('{name} has {count:d} contract(s).'))
def has_n_contracts(name, count):
    assert Contract.objects.filter(
        customer__first_name=name,
        status__name="signed"
    ).count() == count
