import pytest
from crm.models import Event, Contract, Customer
from django.utils import timezone
import datetime


@pytest.fixture
def event(contract, sales_employee2, support_employee2):
    return Event.objects.create(
        attendee=4,
        event_date=timezone.now(),
        support_contact=support_employee2,
        contract=Contract.objects.create(
            amount=7.2,
            payment_due=timezone.now(),
            customer=Customer.objects.create(
                first_name='Mick',
                last_name='Codeur',
                sales_contact=sales_employee2
            )
        ),
    )


@pytest.fixture
def events(contracts, support_employee):
    res = []
    for i, contract in enumerate(contracts):
        res.append(Event.objects.create(
            attendee=i,
            event_date=timezone.make_aware(datetime.datetime(year=2023, month=3, day=1 + i)),
            contract=contract,
            support_contact=support_employee
        ))

    for i in range(0, 4):
        res.append(Event.objects.create(
            attendee=56,
            event_date=timezone.make_aware(datetime.datetime(year=2024, month=9, day=5)),
            support_contact=support_employee,
            contract=Contract.objects.create(
                amount=7.3,
                payment_due=timezone.now(),
                customer=Customer.objects.create()
            )
        ))

    return res
