from fixtures import *


def quick_event(contact=None):
    obj = {
        'attendee':14,
        'event_date': timezone.now(),
        'notes': 'my event',
        'contract': Contract.objects.create(
            amount=7.2,
            payment_due=timezone.now()
        ),
    }

    if contact is not None:
        obj['support_contact'] = contact

    return obj


@pytest.mark.parametrize('employee_str,oracle,count', [
    ('management_employee', status.HTTP_200_OK, 5),
    ('sales_employee', status.HTTP_403_FORBIDDEN, 0),
    ('support_employee', status.HTTP_200_OK, 0),
    ('support_employee__customer', status.HTTP_200_OK, 2),
])
def test_event_list(client, request, employee_str, oracle, count):
    my_employee = request.getfixturevalue(employee_str)
    client.force_login(my_employee)

    before_count = Event.objects.count()

    Event.objects.create(**quick_event())
    Event.objects.create(**quick_event())
    if employee_str == 'support_employee__customer':
        Event.objects.create(**quick_event(my_employee))
        Event.objects.create(**quick_event(my_employee))
    else:
        Event.objects.create(**quick_event())
        Event.objects.create(**quick_event())
    Event.objects.create(**quick_event())

    res = client.get(reverse_lazy('crm:events-list'))

    assert oracle == res.status_code
    assert res.status_code != status.HTTP_200_OK \
           or count == len(res.data) - before_count


@pytest.mark.parametrize('employee_str,own,oracle', [
    ('management_employee', False, status.HTTP_200_OK),
    ('sales_employee', False, status.HTTP_403_FORBIDDEN),
    ('support_employee', False, status.HTTP_403_FORBIDDEN),
    ('support_employee', True, status.HTTP_200_OK),
])
def test_event_retrieve(client, request, employee_str, own, oracle):
    my_employee = request.getfixturevalue(employee_str)
    client.force_login(my_employee)

    ev = Event.objects.create(**quick_event(my_employee if own else None))

    res = client.get(reverse_lazy('crm:events-detail', kwargs={
        'pk': ev.id
    }))

    assert oracle == res.status_code


@pytest.mark.parametrize('employee_str,oracle', [
    ('management_employee', status.HTTP_201_CREATED),
    ('sales_employee', status.HTTP_201_CREATED),
    ('support_employee', status.HTTP_403_FORBIDDEN),
])
def test_event_create(client, request, contract, employee_str, oracle):
    my_employee = request.getfixturevalue(employee_str)
    client.force_login(my_employee)

    res = client.post(reverse_lazy('crm:events-list'), {
        'attendee': 14,
        'event_date': timezone.now(),
        'notes': 'event notes',
        'contract': contract.id
    })

@pytest.mark.parametrize('employee_str,own,oracle', [
    ('management_employee', False, status.HTTP_200_OK),
    ('sales_employee', False, status.HTTP_403_FORBIDDEN),
    ('support_employee', False, status.HTTP_403_FORBIDDEN),
    ('support_employee', True, status.HTTP_200_OK),
])
def test_event_update(client, event,
                      request, contract,
                      employee_str, own, oracle):
    my_employee = request.getfixturevalue(employee_str)
    client.force_login(my_employee)

    if own:
        event.support_contact = my_employee
        event.save()

    res = client.put(reverse_lazy('crm:events-detail', kwargs={
        'pk': event.id
    }), {
        'attendee': 14,
        'event_date': timezone.now(),
        'notes': 'event notes',
        'contract': contract.id
    })

    assert oracle == res.status_code


@pytest.mark.parametrize('employee_str,oracle', [
    ('management_employee', status.HTTP_204_NO_CONTENT),
    ('sales_employee', status.HTTP_403_FORBIDDEN),
    ('support_employee', status.HTTP_403_FORBIDDEN),
])
def test_event_destroy(client, event,
                      request, employee_str, oracle):
    my_employee = request.getfixturevalue(employee_str)
    client.force_login(my_employee)

    res = client.delete(reverse_lazy('crm:events-detail', kwargs={
        'pk': event.id
    }))

    assert oracle == res.status_code
