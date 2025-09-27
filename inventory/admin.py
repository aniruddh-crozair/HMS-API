from django.contrib import admin
from inventory.models import Hoarding, HoardingAddress, HoardingImage

admin.site.register(Hoarding)
admin.site.register(HoardingAddress)
admin.site.register(HoardingImage)
