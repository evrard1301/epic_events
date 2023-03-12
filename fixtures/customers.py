import pytest
from crm.models import Customer


@pytest.fixture
def customer(db):
    return Customer.objects.create(first_name='Alice')