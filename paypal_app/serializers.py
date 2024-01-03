# serializers.py

from rest_framework import serializers

class PayPalPaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3)
    # Add other necessary fields as per your requirements
