from fixtures import *


@pytest.mark.parametrize('employee_str,oracle', [
    ('noteam_employee', status.HTTP_403_FORBIDDEN),
    ('management_employee', status.HTTP_201_CREATED),
    ('sales_employee', status.HTTP_403_FORBIDDEN),
    ('support_employee', status.HTTP_403_FORBIDDEN)
])
def test_users_create(client, request, employee_str, oracle):
    my_employee = request.getfixturevalue(employee_str)
    client.force_login(my_employee)

    res = client.post(reverse_lazy('crm:users-list'), {
        'username': 'dan',
        'first_name': 'Dan',
        'last_name': 'Dredden',
        'password': 'danpassword',
        'email': 'dan@email.com'
    })

    assert oracle == res.status_code


@pytest.mark.parametrize('employee_str,oracle', [
    ('noteam_employee', status.HTTP_403_FORBIDDEN),
    ('management_employee', status.HTTP_200_OK),
    ('sales_employee', status.HTTP_403_FORBIDDEN),
    ('support_employee', status.HTTP_403_FORBIDDEN)
])
def test_users_list(client, request, employee_str, oracle):
    my_employee = request.getfixturevalue(employee_str)
    client.force_login(my_employee)
    res = client.get(reverse_lazy('crm:users-list'))
    assert oracle == res.status_code


@pytest.mark.parametrize('employee_str,oracle', [
    ('noteam_employee', status.HTTP_403_FORBIDDEN),
    ('management_employee', status.HTTP_200_OK),
    ('sales_employee', status.HTTP_403_FORBIDDEN),
    ('support_employee', status.HTTP_403_FORBIDDEN)
])
def test_users_retrieve(client, request, employee_str, oracle):
    my_employee = request.getfixturevalue(employee_str)
    client.force_login(my_employee)
    user = User.objects.create_user(username='benoit', password='benoitpassword')
    res = client.get(reverse_lazy('crm:users-detail', kwargs={
        'pk': user.id
    }))
    assert oracle == res.status_code


@pytest.mark.parametrize('employee_str,oracle', [
    ('noteam_employee', status.HTTP_403_FORBIDDEN),
    ('management_employee', status.HTTP_200_OK),
    ('sales_employee', status.HTTP_403_FORBIDDEN),
    ('support_employee', status.HTTP_403_FORBIDDEN)
])
def test_users_update(client, request, employee_str, oracle):
    my_employee = request.getfixturevalue(employee_str)
    client.force_login(my_employee)
    user = User.objects.create_user(username='benoit', password='benoitpassword')
    res = client.put(reverse_lazy('crm:users-detail', kwargs={
        'pk': user.id
    }), {
        'username': 'maxime',
        'email': 'maxime.moulin@email.com'
    })

    assert oracle == res.status_code


@pytest.mark.parametrize('employee_str,oracle', [
    ('noteam_employee', status.HTTP_403_FORBIDDEN),
    ('management_employee', status.HTTP_204_NO_CONTENT),
    ('sales_employee', status.HTTP_403_FORBIDDEN),
    ('support_employee', status.HTTP_403_FORBIDDEN)
])
def test_users_destroy(client, request, employee_str, oracle):
    my_employee = request.getfixturevalue(employee_str)
    client.force_login(my_employee)
    user = User.objects.create_user(username='benoit', password='benoitpassword')
    res = client.delete(reverse_lazy('crm:users-detail', kwargs={
        'pk': user.id
    }))
    assert oracle == res.status_code
