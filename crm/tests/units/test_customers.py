from fixtures import *
from crm.models import Customer


@pytest.mark.parametrize('employee_str,oracle', [
    ('management_employee', status.HTTP_200_OK),
    ('sales_employee', status.HTTP_200_OK),
    ('support_employee', status.HTTP_200_OK),
])
def test_customers_list(client, request, employee_str, oracle):
    my_employee = request.getfixturevalue(employee_str)
    client.force_login(my_employee)

    Customer.objects.create(first_name='Alice')

    if employee_str == 'management_employee':
        Customer.objects.create(first_name='Bob')
    else:
        Customer.objects.create(first_name='Bob', sales_contact=my_employee)

    Customer.objects.create(first_name='Claire')

    res = client.get(reverse_lazy('crm:customers-list'))

    assert oracle == res.status_code
    assert Customer.objects.count() == len(res.data)


@pytest.mark.parametrize('employee_str,oracle', [
    ('management_employee', status.HTTP_200_OK),
    ('sales_employee', status.HTTP_200_OK),
    ('sales_employee__customer', status.HTTP_200_OK),
    ('support_employee', status.HTTP_200_OK),
    ('support_employee__customer', status.HTTP_200_OK),
])
def test_customers_retrieve(client, customer, request, employee_str, oracle):
    my_employee = request.getfixturevalue(employee_str)
    client.force_login(my_employee)

    res = client.get(reverse_lazy('crm:customers-detail', kwargs={
        'pk': customer.id
    }))

    assert oracle == res.status_code


@pytest.mark.parametrize('employee_str,oracle', [
    ('management_employee', status.HTTP_201_CREATED),
    ('sales_employee', status.HTTP_201_CREATED),
    ('support_employee', status.HTTP_403_FORBIDDEN),
])
def test_customers_create(client, sales_employee2,
                          request, employee_str, oracle):
    my_employee = request.getfixturevalue(employee_str)
    client.force_login(my_employee)
    res = client.post(reverse_lazy('crm:customers-list'), {
        'first_name': 'Jack',
        'last_name': 'Johnson',
        'email': 'jjohnson@email.com',
        'phone': '000-000-000',
        'mobile': '000-000-000',
        'company': 'JackInc',
        'sales_contact': sales_employee2.id
    })

    assert oracle == res.status_code


@pytest.mark.parametrize('employee_str,oracle', [
    ('management_employee', status.HTTP_200_OK),
    ('sales_employee', status.HTTP_403_FORBIDDEN),
    ('sales_employee__customer', status.HTTP_200_OK),
    ('support_employee', status.HTTP_403_FORBIDDEN),
])
def test_customers_update(client, customer, request, employee_str, oracle):
    my_employee = request.getfixturevalue(employee_str)
    client.force_login(my_employee)

    res = client.put(reverse_lazy('crm:customers-detail', kwargs={
        'pk': customer.id
    }), {
        'first_name': 'Kali',
        'last_name': 'Kokon',
        'email': 'kkokon@email.com',
        'phone': '000-000-000',
        'mobile': '000-000-000',
        'company': 'KokonInc',
        'sales_contact': customer.sales_contact.id
    })

    assert oracle == res.status_code


@pytest.mark.parametrize('employee_str,oracle', [
    ('management_employee', status.HTTP_200_OK),
    ('sales_employee', status.HTTP_403_FORBIDDEN),
    ('sales_employee__customer', status.HTTP_200_OK),
    ('support_employee', status.HTTP_403_FORBIDDEN),
])
def test_customers_partial_update(client, customer, request, employee_str, oracle):
    my_employee = request.getfixturevalue(employee_str)
    client.force_login(my_employee)

    res = client.patch(reverse_lazy('crm:customers-detail', kwargs={
        'pk': customer.id
    }), {
        'first_name': 'Gaston'
    })

    assert oracle == res.status_code
    if oracle == status.HTTP_200_OK:
        assert 'Gaston' == Customer.objects.get(pk=customer.id).first_name




@pytest.mark.parametrize('employee_str,oracle', [
    ('management_employee', status.HTTP_204_NO_CONTENT),
    ('sales_employee', status.HTTP_403_FORBIDDEN),
    ('sales_employee__customer', status.HTTP_204_NO_CONTENT),
    ('support_employee', status.HTTP_403_FORBIDDEN),
])
def test_customers_delete(client, customer, request, employee_str, oracle):
    my_employee = request.getfixturevalue(employee_str)
    client.force_login(my_employee)

    res = client.delete(reverse_lazy('crm:customers-detail', kwargs={
        'pk': customer.id
    }))

    assert oracle == res.status_code
