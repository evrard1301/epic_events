from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


def is_support_validator(user):
    if not user.is_in_group('SupportTeam'):
        raise ValidationError('not a support user')


def is_sales_validator(user):
    if not user.is_in_group('SalesTeam'):
        raise ValidationError('not a sales user')


class User(AbstractUser):
    def is_in_group(self, grp):
        return grp in [g.name for g in self.groups.all()]


class Customer(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    company = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        validators=[is_sales_validator]
    )


class ContractStatus(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name_plural = 'Contract status'


class Contract(models.Model):
    amount = models.FloatField()
    status = models.ForeignKey(ContractStatus, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    payment_due = models.DateTimeField()
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)


class EventStatus(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name_plural = 'Event status'


class Event(models.Model):
    attendee = models.IntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(EventStatus, on_delete=models.SET_NULL, null=True)
    support_contact = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        validators=[is_support_validator]
    )

    contract = models.OneToOneField(Contract, on_delete=models.CASCADE)