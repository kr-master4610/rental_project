from django.db import models
from django.db import models
from django.conf import settings


class Listing(models.Model):
    APARTMENT = 'apartment'
    HOUSE = 'house'
    STUDIO = 'studio'

    TYPE_CHOICES = [
        (APARTMENT, 'Квартира'),
        (HOUSE, 'Дом'),
        (STUDIO, 'Студия'),
    ]

    landlord = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listings'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)  # Город или район в Германии
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rooms = models.IntegerField()
    housing_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=APARTMENT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
# Create your models here.
class Booking(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Бронь {self.tenant.email} на {self.listing.title}"
