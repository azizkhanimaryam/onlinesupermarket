from django.urls import path
from .views import PaymentVerifyView

urlpatterns = [
    path('payment/verify/', PaymentVerifyView.as_view(), name='payment_verify'),
]
