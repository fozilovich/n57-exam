from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app_payment.views import MonthViewSet, PaymentTypeViewSet, PaymentViewSet

app_name = 'payments'

router = DefaultRouter()
router.register(r'months',MonthViewSet,basename='month')
router.register(r'payment-type',PaymentTypeViewSet,basename='payment-type')
router.register(r'payment',PaymentViewSet,basename='payment')
urlpatterns = [
    path('', include(router.urls)),
]