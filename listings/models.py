from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Listing(models.Model):
    """
    Model representing a real estate listing.
    """
    APARTMENT = 'apartment'
    HOUSE = 'house'
    STUDIO = 'studio'

    TYPE_CHOICES = [
        (APARTMENT, 'Apartment'),
        (HOUSE, 'House'),
        (STUDIO, 'Studio'),
    ]

    landlord = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,  # Prevent deletion if listings exist
        related_name='listings'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1.00, message="Price must be greater than zero.")]
    )
    rooms = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Must have at least 1 room."),
            MaxValueValidator(20, message="Maximum 20 rooms allowed.")
        ]
    )
    housing_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=APARTMENT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title