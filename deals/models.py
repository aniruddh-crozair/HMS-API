from django.db import models
from django.db.models import Sum
from customers.models import Customer
from inventory.models import Hoarding

class Deal(models.Model):
    """
    Represents a pre-invoice booking agreement.
    Linked to a single Customer.
    Tracks total amount, advance paid, campaign period, and status.
    """
    DEAL_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled")
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="deals")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    advance_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    deal_status = models.CharField(max_length=16, choices=DEAL_STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def update_total_amount(self):
        total = self.deal_hoardings.aggregate(total=Sum('booked_rate'))['total'] or 0
        self.total_amount = total
        self.save(update_fields=['total_amount'])

    def __str__(self):
        return f"{self.id} - {self.customer.name}"

    class Meta:
        db_table = "deal"
        ordering = ["-created_at"]



class DealHoarding(models.Model):
    """
    Many-to-many mapping between Deal and Hoardings
    For Tracking purpose only
    """
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name="deal_hoardings")
    hoarding = models.ForeignKey(Hoarding, on_delete=models.CASCADE, related_name="deal_hoardings")
    booked_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    duration_months = models.PositiveIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Calculate the duration months automatically
        Calculate the price for each hoarding details
        """
        self.duration_months = (self.deal.end_date.year - self.deal.start_date.year) * 12 + \
                                (self.deal.end_date.month - self.deal.start_date.month) + 1

        if not self.booked_rate and self.hoarding.monthly_rate:
                self.booked_rate = self.hoarding.monthly_rate * self.duration_months
        super().save(*args, **kwargs)
    
        # Auto update deal total
        self.deal.update_total_amount()
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.deal.update_total_amount()

    def __str__(self):
        return f"{self.hoarding.title} deal with {self.deal.customer}"

    class Meta:
        db_table = "deal_hoarding"
        unique_together = ("deal", "hoarding")



