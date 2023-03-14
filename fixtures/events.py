import pytest
from crm.models import Event
from django.utils import timezone


@pytest.fixture
def event(contract):
    return Event.objects.create(
        attendee=4,
        event_date=timezone.now(),
        contract=contract
    )