from django.contrib import admin
from .models import Hoarding, HoardingAddress, HoardingImage

admin.site.register(HoardingImage)
admin.site.register(HoardingAddress)

class HoardingAddressInline(admin.TabularInline):
    model = HoardingAddress
    extra = 1  # Number of extra empty forms
    fields = ['city', 'latitude', 'longitude', 'location_type']
    readonly_fields = ['created_at']

class HoardingImageInline(admin.TabularInline):
    model = HoardingImage
    extra = 1
    fields = ['image', 'is_primary', 'caption']
    readonly_fields = ['uploaded_at']

@admin.register(Hoarding)
class HoardingAdmin(admin.ModelAdmin):
    list_display = [
        "owner",
        "title",
        "description",
        "mounting_type",
        "height",
        "length",
        "breadth",
        "facing",
        "illumination",
        "material_type",
        "suggested_purpose",
        "monthly_rate",
        "availability_status",
        "is_available",
        "is_verified",
    ]
    search_fields = ["title", "owner__name", "description"]
    list_filter = ["mounting_type", "facing", "illumination", "availability_status"]
    inlines = [HoardingAddressInline, HoardingImageInline]
