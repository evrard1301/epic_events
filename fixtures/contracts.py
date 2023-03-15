import pytest
from crm.models import Contract
from django.utils import timezone
import datetime


@pytest.fixture
def contract(db):
    return Contract.objects.create(
        amount=7.2,
        payment_due=timezone.now()
    )


@pytest.fixture
def contracts(customers):
    res = []

    for i in range(0, 7):
        c = Contract.objects.create(
            amount=float(i),
            payment_due=timezone.now(),
            customer=customers[list(customers)[i]]
        )
        c.date_created = timezone.make_aware(datetime.datetime(year=2023, month=3, day=(14 + i)))
        c.save()
        res.append(c)

    for i in range(0, 3):
        c = Contract.objects.create(
            amount=45.0,
            payment_due=timezone.now(),
            customer=customers[list(customers)[0]]
        )
        c.date_created = timezone.make_aware(datetime.datetime(year=2023, month=4, day=13))
        c.save()
        res.append(c)

    return res