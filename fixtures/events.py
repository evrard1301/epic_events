import pytest
from crm.models import Event, Contract
from django.utils import timezone
import datetime


@pytest.fixture
def event(contract):
    return Event.objects.create(
        attendee=4,
        event_date=timezone.now(),
        contract=contract
    )


@pytest.fixture
def events(contracts):
    res = []
    for i, contract in enumerate(contracts):
        res.append(Event.objects.create(
            attendee=i,
            event_date=timezone.make_aware(datetime.datetime(year=2023, month=3, day=1 + i)),
            contract=contract
        ))

    for i in range(0, 4):
        res.append(Event.objects.create(
            attendee=56,
            event_date=timezone.make_aware(datetime.datetime(year=2024, month=9, day=5)),
            contract=Contract.objects.create(
                amount=7.3,
                payment_due=timezone.now()
            )
        ))

    return res
