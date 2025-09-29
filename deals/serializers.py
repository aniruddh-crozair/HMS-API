from rest_framework import serializers
from .models import Deal, DealHoarding

from inventory.serializers import HoardingSerializer
from customers.serializers import CustomerSerializer

class DealHoardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealHoarding
        fields = [
            "id",
            "hoarding",
            "booked_rate",
            "duration_months"
        ]


class DealSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    deal_hoardings = DealHoardingSerializer(many=True, read_only=True)
    class Meta:
        model = Deal
        fields = [
            'id', 'customer', 'total_amount', 
            'advance_amount', 'start_date', 
            'end_date', 'deal_status', 'created_at', 
            'deal_hoardings'
        ]