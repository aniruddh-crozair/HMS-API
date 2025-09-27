from django.db import models
from django.utils import timezone
from deals.models import Deal

class Invoice(models.Model):
    """
    Represents the detail related to amount to be paid and remaining so on
    """
    STATUS_CHOICES =[
        ('unpaid', 'Unpaid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Fully Paid'),
    ]
    deal = models.OneToOneField(Deal, on_delete=models.CASCADE, related_name='invoice')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remaining_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')

    issued_date = models.DateField(default=timezone.now)
    due_date = models.DateField(null=True, blank=True)

    
    def update_status(self):
        """
        Auto update the status based on amount against hoarding deals.
        """
        if self.paid_amount >= self.total_amount:
            self.status = 'paid'
            self.remaining_amount = 0
        elif 0 < self.paid_amount < self.total_amount:
            self.status = 'partial'
            self.remaining_amount = self.total_amount - self.paid_amount
        else:
            self.status = 'unpaid'
            self.remaining_amount = self.total_amount

        self.save(update_fields=['status', 'remaining_amount'])
    
    def __str__(self):
        return f"Invoice #{self.id} - Deal {self.deal.id}"