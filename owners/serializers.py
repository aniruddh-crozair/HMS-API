from rest_framework import serializers
from .models import Owner, OwnerContact, OwnerAddress

class OwnerContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = OwnerContact
        fields = "__all__"

class OwnerAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = OwnerAddress
        fields = "__all__"

class OwnerSerializer(serializers.ModelSerializer):
    contacts = OwnerContactSerializer(many=True, read_only=True)
    addresses = OwnerAddressSerializer(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ['id', 'name', 'created_at', 'contacts', 'addresses']