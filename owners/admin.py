from django.contrib import admin
from owners.models import Owner, OwnerContact, OwnerAddress

admin.site.register(Owner)
admin.site.register(OwnerContact)
admin.site.register(OwnerAddress)
