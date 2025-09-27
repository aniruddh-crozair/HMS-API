from django.contrib import admin
from deals.models import Deal, DealHoarding

# admin.site.register(Deal)
admin.site.register(DealHoarding)


class DealHoardingInline(admin.TabularInline):
    model = DealHoarding
    extra = 0
    fields = ("hoarding", "duration_months", "booked_rate")



@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "total_amount", "deal_status")
    inlines = [DealHoardingInline]