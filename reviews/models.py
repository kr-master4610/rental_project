from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from listings.models import Listing

class Review(models.Model):
    """
    Model representing a user review for a listing.
    """
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='reviews')

    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="Rating must be at least 1."),
            MaxValueValidator(5, message="Rating cannot be higher than 5.")
        ]
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.author.email} on {self.listing.title} ({self.rating}★)"