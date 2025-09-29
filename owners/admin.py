from django.contrib import admin
from owners.models import Owner, OwnerContact, OwnerAddress

# admin.site.register(Owner)
admin.site.register(OwnerContact)
admin.site.register(OwnerAddress)

class OwnerContactInline(admin.TabularInline):
    model = OwnerContact
    fields = (
        "name",
        "phone",
        "email"
    )

class OwnerAddressInline(admin.TabularInline):
    model = OwnerAddress
    fields = (
        "address_line1",
        "city",
        "state",
        "country"
    )

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [OwnerContactInline, OwnerAddressInline]