from fixtures import *


@pytest.mark.parametrize('query,search,attr,oracle,count', [
    ('name', 'Catty', 'first_name', 'Claire', 1),
    ('name', 'Domann', 'first_name', 'Dan', 1),
    ('name', 'Worry', 'first_name', 'Walter', 0),

    ('email', 'bob.bishop@email.com', 'first_name', 'Bob', 1),
    ('email', 'sam.fisher@email.com', 'first_name', '', 0),
])
def test_search_customers(client, management_employee, customers,
                          query, search,
                          oracle, attr,
                          count):

    client.force_login(management_employee)

    res = client.get(reverse_lazy('crm:customers-list') + f'?{query}={search}')

    assert count == len(res.data)
    assert len(res.data) == 0 or oracle == res.data[0][attr]


@pytest.mark.parametrize('query,search,attr,oracle,count', [
    ('name', 'Ecte', 'amount', 4.0, 1),
    ('name', 'Zuzu', '', 0, 0),
    ('email', 'fred.fuero@email.com', 'amount', 5.0, 1),
    ('email', 'james.nodol@email.com', '', 0, 0),

    ('date', '09/02/2027', '', 0, 0),
    ('date', '03/16/2023', 'amount', 2.0, 1),
    ('date', '04/13/2023', 'amount', 45.0, 3),

    ('amount', 3141592653.2, '', 0, 0),
    ('amount', 3.0, 'amount', 3.0, 1),
    ('amount', 45.0, 'amount', 45.0, 3),

])
def test_search_contracts(client, management_employee, contracts,
                          query, search,
                          attr, oracle,
                          count):

    client.force_login(management_employee)

    res = client.get(reverse_lazy('crm:contracts-list') + f'?{query}={search}')

    assert count == len(res.data)
    assert len(res.data) == 0 or oracle == res.data[0][attr]


@pytest.mark.parametrize('query,search,attr,oracle,count', [
    ('name', 'Catty', 'attendee', 2, 1),
    ('name', 'Azerty', '', 0, 0),

    ('email', 'sgary.gimson@email.com', 'attendee', 6, 1),
    ('email', 'james.coconuts@email.com', '', 0, 0),
    ('date', '09/05/24', 'attendee', 56, 4),
    ('date', '03/03/2023', 'attendee', 2, 1),
    ('date', '03/03/2028', '', 0, 0),

])
def test_search_events(client, management_employee, events,
                       query, search,
                       attr, oracle,
                       count):

    client.force_login(management_employee)
    res = client.get(reverse_lazy('crm:events-list') + f'?{query}={search}')
    assert count == len(res.data)
    assert len(res.data) == 0 or oracle == res.data[0][attr]
