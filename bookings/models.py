from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from listings.models import Listing

class Booking(models.Model):
    """
    Model representing a booking of a listing by a user.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    listing = models.ForeignKey(
        Listing,
        on_delete=models.PROTECT,  # Protect prevents deletion if a booking exists
        related_name='bookings'
    )
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='bookings'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """
        Validate dates to ensure logical booking consistency.
        """
        if self.start_date < timezone.now().date():
            raise ValidationError("Start date cannot be in the past.")
        if self.end_date < self.start_date:
            raise ValidationError("End date cannot be earlier than start date.")

    def save(self, *args, **kwargs):
        """
        Full clean before saving to ensure model-level validation.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.id} - {self.status}"