from django.urls import path
from crm import views
from rest_framework.routers import SimpleRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

app_name = 'crm'

router = SimpleRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('customers', views.CustomerViewSet, basename='customers')
router.register('events', views.EventViewSet, basename='events')
router.register('contracts', views.ContractViewSet, basename='contracts')

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login-refresh')
] + router.urls