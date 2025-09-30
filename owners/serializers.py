from rest_framework import serializers
from .models import Owner, OwnerContact, OwnerAddress

class OwnerContactSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OwnerContact
        fields = "__all__"

class OwnerAddressSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OwnerAddress
        fields = "__all__"

class OwnerSerializer(serializers.ModelSerializer):
    contacts = OwnerContactSerializer(many=True)
    addresses = OwnerAddressSerializer(many=True)

    class Meta:
        model = Owner
        fields = ['id', 'name', 'created_at', 'contacts', 'addresses']
    
    def create(self, validated_data):
        # Extract nested data
        contacts_data = validated_data.pop("contacts", [])
        addresses_data = validated_data.pop("addresses", [])

        # Create Owner
        owner = Owner.objects.create(**validated_data)

        # Create contacts linked to owner
        for contact_data in contacts_data:
            OwnerContact.objects.create(owner=owner, **contact_data)

        # Create addresses linked to owner
        for address_data in addresses_data:
            OwnerAddress.objects.create(owner=owner, **address_data)

        return owner
