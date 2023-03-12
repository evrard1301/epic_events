import pytest
from fixtures import *

@pytest.mark.parametrize('username,password,oracle', [
    ('Alice', 'alicepassword', status.HTTP_401_UNAUTHORIZED),
    ('Dan', 'alicepassword', status.HTTP_401_UNAUTHORIZED),
    ('Alice', 'danpassword', status.HTTP_401_UNAUTHORIZED),
    ('Dan', 'danpassword', status.HTTP_200_OK),
])
def test_login(client, username, password, oracle):
    get_user_model().objects.create_user(username='Dan',
                                         password='danpassword')

    res = client.post(reverse_lazy('crm:login'), {
        'username': username,
        'password': password
    })

    assert oracle == res.status_code
