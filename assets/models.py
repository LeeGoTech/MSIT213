from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum

# TOPIC 1: Custom User Models
class User(AbstractUser):
    """
    Custom user model to allow for future expansion (e.g., adding Department fields).
    """
    is_manager = models.BooleanField(default=False)

# TOPIC 2: Abstract Base Classes (Code Reuse)
class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    'created' and 'modified' fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Asset(TimeStampedModel):
    """
    Concrete model inheriting from TimeStampedModel.
    """
    ASSET_TYPES = (
        ('LAPTOP', 'Laptop'),
        ('MONITOR', 'Monitor'),
        ('PHONE', 'Phone'),
        ('FURNITURE', 'Furniture'),
    )

    name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    # DecimalField is best practice for currency/value
    cost = models.DecimalField(max_digits=10, decimal_places=2) 
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')
    
    def __str__(self):
        return f"{self.name} ({self.get_asset_type_display()})"