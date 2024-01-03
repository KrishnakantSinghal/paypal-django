"""
views.py
"""

from rest_framework.views import APIView
from rest_framework.response import Response
import paypalrestsdk
from django.conf import settings
from django.shortcuts import render
from .serializers import PayPalPaymentSerializer

# from analytical import track_page_view

paypalrestsdk.configure(
    {
        "mode": settings.PAYPAL_MODE,  # Set to 'live' for production
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET,
    }
)


class PayPalPaymentView(APIView):
    """
    class
    """

    def post(self, request):
        """
        function
        """
        serializer = PayPalPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_data = serializer.validated_data

        payment = paypalrestsdk.Payment(
            {
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "transactions": [
                    {
                        "amount": {
                            "total": str(payment_data["amount"]),
                            "currency": payment_data["currency"],
                        },
                        # Add other transaction details as needed
                    }
                ],
                "redirect_urls": {
                    "return_url": "http://127.0.0.1:8000/payment-success",
                    "cancel_url": "http://127.0.0.1:8000/cancel-payment",
                },
            }
        )

        if payment.create():
            # Payment created successfully
            approval_url = [
                link.href for link in payment.links if link.rel == "approval_url"
            ][0]
            return Response({"approval_url": approval_url})
        return Response({"error": payment.error})


def render_success(request):
    """
    function
    """
    return render(request, "payment_success.html")


def cancel_payment(request):
    """
    function
    """
    return render(request, "payment_fails.html")
