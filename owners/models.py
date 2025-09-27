from django.db import models

class Owner(models.Model):
    """
    Represents a Hoarding / Billboard owner (Vendor / Media)
    """
    name = models.CharField(max_length=255, help_text="Owner's business name")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 
    
    class Meta:
        db_table = "Owner"
        ordering = ["name"]

class OwnerContact(models.Model):
    """
    Multiple contacts for each owner
    """
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.owner.name})"
    
    class Meta:
        db_table = "owner_contact"
        ordering = ["owner", "name"]


class OwnerAddress(models.Model):
    """
    Multiple addresses per owner (branch, office, etc.)
    """
    owner = models.ForeignKey(Owner,on_delete=models.CASCADE,related_name="addresses")
    address_line1 = models.CharField(max_length=512)
    address_line2 = models.CharField(max_length=512, blank=True)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    pincode = models.CharField(max_length=32)
    country = models.CharField(max_length=128, default="India")

    def __str__(self):
        return f"{self.address_line1}, {self.city} ({self.owner.name})"

    class Meta:
        db_table = "owner_address"
        ordering = ["owner", "city"]