# urls.py

from django.urls import path
from .views import PayPalPaymentView, render_success, cancel_payment

urlpatterns = [
    # Other URLs
    path("paypal-payment/", PayPalPaymentView.as_view(), name="paypal-payment"),
    path("payment-success/", render_success),
    path("cancel-payment", cancel_payment),
]
