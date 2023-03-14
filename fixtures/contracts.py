import pytest
from crm.models import Contract
from django.utils import timezone


@pytest.fixture
def contract(db):
    return Contract.objects.create(
        amount=7.2,
        payment_due=timezone.now()
    )