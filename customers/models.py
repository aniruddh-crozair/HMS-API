from django.db import models

class Customer(models.Model):
    """
    Advertiser / Client who books hoardings
    """
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "customer"
        ordering = ["name"]

class CustomerAddress(models.Model):
    """
    Multiple addresses per customer (billing, office)
    """
    ADDRESS_TYPE_CHOICES = [
        ("billing", "Billing"),
        ("office", "Office"),
        ("other", "Other")
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=32, choices=ADDRESS_TYPE_CHOICES, default="office")
    address_line1 = models.CharField(max_length=512)
    address_line2 = models.CharField(max_length=512, blank=True)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    pincode = models.CharField(max_length=32)
    country = models.CharField(max_length=128, default="India")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.address_line1}, {self.city} ({self.customer.name})"

    class Meta:
        db_table = "customer_address"
        ordering = ["customer", "city"]