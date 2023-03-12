from .client import *
from .employee import *
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework import status
from crm.models import User