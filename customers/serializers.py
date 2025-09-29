from rest_framework import serializers
from .models import Customer, CustomerAddress


class CustomerAddressSerializer(serializers.ModelSerializer):
    # Make customer read-only so client doesn't need to send it
    customer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CustomerAddress
        fields = ['id', 'address_type', 'address_line1', 'address_line2', 'city', 'state', 'pincode', 'country', 'customer', 'created_at']

class CustomerSerializer(serializers.ModelSerializer):
    # Nested address list (Read-Only)
    addresses = CustomerAddressSerializer(many=True, required=False)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'email', 'created_at', 'addresses',]

    def create(self, validated_data):
        """
        Create a Customer instance along with multiple CustomerAddress instances.
        Args:
            validated_data (dict): Validated data from the serializer, including a key 'addresses'
                                   which is a list of address dictionaries.
        Returns:
            Customer: The created Customer instance with related addresses.
        """
        # Pop addresses if present, default empty list
        addresses_data = validated_data.pop('addresses', [])
        customer = Customer.objects.create(**validated_data)

        # Create each address and link to the new customer
        for addr_data in addresses_data:
            CustomerAddress.objects.create(customer=customer, **addr_data)

        return customer