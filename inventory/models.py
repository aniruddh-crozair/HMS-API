from django.db import models
from owners.models import Owner

class Hoarding(models.Model):
    """
    Stores the hoarding details
    """
    MOUNTING_CHOICES = [
        ("Unipole", "Unipole"),
        ("Multipole", "Multipole"),
        ("Cantilever", "Cantilever"),
        ("Gantry", "Gantry"),
    ]

    FACING_CHOICES = [
        ("North", "North"), ("South", "South"), ("East", "East"), ("West", "West"),
        ("Northeast", "Northeast"), ("Northwest", "Northwest"),
        ("Southeast", "Southeast"), ("Southwest", "Southwest")
    ]

    ILLUMINATION_CHOICES = [
        ("External", "External"), ("Internal", "Internal")
    ]
    
    MATERIAL_CHOICES = [
        ("Timber", "Timber"), ("Steel", "Steel"),
        ("Water-Filled Barriers", "Water-Filled Barriers"),
        ("Concrete", "Concrete"), ("Mesh Panel", "Mesh Panel")
    ]

    
    PURPOSE_CHOICES = [
        ("Event", "Event"), ("Retail", "Retail"), ("Community Engagement", "Community Engagement"),
        ("Development", "Development"), ("Informational", "Informational"), ("Other", "Other")
    ]

    STATUS_CHOICES = [
        ("available", "Available"), ("booked", "Booked"), ("maintenance", "Maintenance")
    ]

    WEATHER_CHOICES = [
        ("UV-coated vinyl", "UV-coated vinyl"), ("Aluminum", "Aluminum"), ("Other", "Other")
    ]

    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="hoardings")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    mounting_type = models.CharField(max_length=32, choices=MOUNTING_CHOICES)
    height = models.FloatField()
    length = models.FloatField()
    breadth = models.FloatField()
    facing = models.CharField(max_length=16, choices=FACING_CHOICES)
    illumination = models.CharField(max_length=16, choices=ILLUMINATION_CHOICES)
    material_type = models.CharField(max_length=32, choices=MATERIAL_CHOICES)
    suggested_purpose = models.CharField(max_length=32, choices=PURPOSE_CHOICES)
    monthly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    availability_status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="available")
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    is_available = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    master_img_url = models.ImageField(upload_to='hoardings_images', null=True)
    weather_resistant_material = models.CharField(max_length=32, choices=WEATHER_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "hoarding"
        ordering = ["title"]


class HoardingAddress(models.Model):
    """
    Stores the hoarding address.
    """
    LOCATION_CHOICES = [
        ("High traffic", "High traffic"),
        ("Residential", "Residential"),
        ("Commercial", "Commercial"),
        ("Highway", "Highway"),
        ("Other", "Other")
    ]

    hoarding = models.ForeignKey(Hoarding, on_delete=models.CASCADE, related_name="addresses")
    address_line = models.CharField(max_length=512)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    pincode = models.CharField(max_length=32)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    location_type = models.CharField(max_length=32, choices=LOCATION_CHOICES, default="Other")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.address_line}, {self.city}"

    class Meta:
        db_table = "hoarding_address"


class HoardingImage(models.Model):
    """
    Store multiple images of hoarding with one main display image the image checked as primary key
    """
    hoarding = models.ForeignKey(Hoarding, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='hoardings_images', null=True)
    is_primary = models.BooleanField(default=False)
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.hoarding.title}"

    class Meta:
        db_table = "hoarding_image"


class Maintenance(models.Model):
    """
    Maintenance stores the maintenance details of hoardings
    """
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled")
    ]

    hoarding = models.ForeignKey(Hoarding, on_delete=models.CASCADE, related_name="maintenance_records")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    maintainer = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="scheduled")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Maintenance for {self.hoarding.title} ({self.status})"

    class Meta:
        db_table = "maintenance"
        ordering = ["-start_date"]