from fixtures import *


@pytest.mark.parametrize('employee_str,own,oracle', [
    ('management_employee', False, status.HTTP_200_OK),
    ('sales_employee', False, status.HTTP_200_OK),
    ('sales_employee', True, status.HTTP_200_OK),
    ('support_employee', False, status.HTTP_200_OK),
])
def test_contracts_list(client, request, customer, employee_str, own, oracle):
    my_employee = request.getfixturevalue(employee_str)
    client.force_login(my_employee)

    Contract.objects.create(
        amount=0.0,
        payment_due=timezone.now(),
        customer=customer
    )

    Contract.objects.create(
        amount=0.0,
        payment_due=timezone.now(),
        customer=customer
    )

    if own:
        for i in range(0, 3):
            c = Contract.objects.create(
                amount=0.0,
                payment_due=timezone.now(),
                customer=customer
            )
            c.customer = Customer.objects.create(
                last_name='Lebowski',
                sales_contact=my_employee,
            )
            c.customer.save()

    Contract.objects.create(
        amount=0.0,
        payment_due=timezone.now(),
        customer=customer
    )

    Contract.objects.create(
        amount=0.0,
        payment_due=timezone.now(),
        customer=customer
    )

    res = client.get(reverse_lazy('crm:contracts-list'))

    assert oracle == res.status_code


@pytest.mark.parametrize('employee_str,own,oracle', [
    ('management_employee', False, status.HTTP_200_OK),
    ('sales_employee', False, status.HTTP_200_OK),
    ('sales_employee', True, status.HTTP_200_OK),
    ('support_employee', False, status.HTTP_200_OK),
])
def test_contracts_retrieve(client, contract,
                            request, employee_str, own, oracle):
    my_employee = request.getfixturevalue(employee_str)
    client.force_login(my_employee)

    if own:
        contract.customer.sales_contact = my_employee
        contract.customer.save()

    res = client.get(reverse_lazy('crm:contracts-detail', kwargs={
        'pk': contract.id
    }))

    assert oracle == res.status_code


@pytest.mark.parametrize('employee_str,oracle', [
    ('management_employee', status.HTTP_201_CREATED),
    ('sales_employee', status.HTTP_201_CREATED),
    ('support_employee', status.HTTP_403_FORBIDDEN),
])
def test_contracts_create(client, customer, request, employee_str, oracle):
    my_employee = request.getfixturevalue(employee_str)
    client.force_login(my_employee)

    res = client.post(reverse_lazy('crm:contracts-list'), {
        'amount': 0.0,
        'payment_due': timezone.now(),
        'customer': customer.id
    })

    assert oracle == res.status_code


@pytest.mark.parametrize('employee_str,own,oracle', [
    ('management_employee', False, status.HTTP_200_OK),
    ('sales_employee', False, status.HTTP_403_FORBIDDEN),
    ('sales_employee', True, status.HTTP_200_OK),
    ('support_employee', False, status.HTTP_403_FORBIDDEN),
])
def test_contracts_update(client, contract,
                          request, employee_str, own, oracle):
    my_employee = request.getfixturevalue(employee_str)
    client.force_login(my_employee)

    if own:
        contract.customer.sales_contact = my_employee
        contract.customer.save()

    res = client.put(reverse_lazy('crm:contracts-detail', kwargs={
        'pk': contract.id
    }), {
        'amount': 0.0,
        'payment_due': timezone.now(),
        'customer': contract.customer.id
    })

    assert oracle == res.status_code


@pytest.mark.parametrize('employee_str,own,oracle', [
    ('management_employee', False, status.HTTP_204_NO_CONTENT),
    ('sales_employee', False, status.HTTP_403_FORBIDDEN),
    ('sales_employee', True, status.HTTP_204_NO_CONTENT),
    ('support_employee', False, status.HTTP_403_FORBIDDEN),
])
def test_contracts_destroy(client, contract,
                           request, employee_str, own, oracle):
    my_employee = request.getfixturevalue(employee_str)
    client.force_login(my_employee)

    if own:
        contract.customer.sales_contact = my_employee
        contract.customer.save()

    res = client.delete(reverse_lazy('crm:contracts-detail', kwargs={
        'pk': contract.id
    }))

    assert oracle == res.status_code


@pytest.mark.parametrize('employee_str,own,oracle', [
    ('management_employee', False, status.HTTP_200_OK),
    ('sales_employee', False, status.HTTP_403_FORBIDDEN),
    ('sales_employee', True, status.HTTP_200_OK),
    ('support_employee', False, status.HTTP_403_FORBIDDEN),
])
def test_contracts_sign(client, contract,
                        request, employee_str, own, oracle):
    my_employee = request.getfixturevalue(employee_str)
    client.force_login(my_employee)

    if own:
        contract.customer.sales_contact = my_employee
        contract.customer.save()

    res = client.post(reverse_lazy('crm:contracts-sign', kwargs={
        'pk': contract.id
    }))

    assert oracle == res.status_code

    if res.status_code == status.HTTP_200_OK:
        contract.refresh_from_db()
        assert contract.status is not None
        assert 'signed' == contract.status.name
