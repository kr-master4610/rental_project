from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from listings.models import Listing


class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')

    # Рейтинг от 1 до 5 звезд
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="Рейтинг не может быть ниже 1"),
            MaxValueValidator(5, message="Рейтинг не может быть выше 5")
        ]
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв от {self.author.email} на {self.listing.title} ({self.rating}★)"
