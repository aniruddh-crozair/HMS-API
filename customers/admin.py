from django.contrib import admin
from customers.models import Customer, CustomerAddress

# admin.site.register(Customer)
admin.site.register(CustomerAddress)

class CustomerAddressInline(admin.TabularInline):
    model = CustomerAddress
    fields = ("address_type", 
              "address_line1", 
              "city", 
              "state",
              "pincode",
              )
    
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email")
    inlines = [CustomerAddressInline]