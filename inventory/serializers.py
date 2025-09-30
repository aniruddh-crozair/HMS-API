from rest_framework import serializers
from .models import Hoarding, HoardingImage, HoardingAddress
from owners.serializers import OwnerSerializer


class HoardingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoardingImage
        fields = ['id', 'image', 'caption']

class HoardingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoardingAddress
        fields = ['address_line', 
                  'city', 'state',
                  'pincode', 
                  'latitude', 'longitude', 
                  'location_type'] 
        
class HoardingSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    images = HoardingImageSerializer(many=True, read_only=True)
    addresses = HoardingAddressSerializer(many=True, read_only=True)

    class Meta:
        model = Hoarding
        fields = [
            'id', 'owner',
            'title', 'description',
            'mounting_type', 'height', 'length', 'breadth', 'facing', 'illumination',
            'material_type', 'is_available', 'is_verified', 'master_img_url', 'weather_resistant_material',
            'created_at', 'updated_at', 'images', 'addresses'
        ]