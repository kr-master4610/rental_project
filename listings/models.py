from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


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

    # Валидатор: цена аренды не может быть отрицательной или нулевой
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1.00, message="Цена должна быть больше нуля.")]
    )

    # Валидатор: в объекте должна быть как минимум 1 комната и не более 20
    rooms = models.IntegerField(
        validators=[
            MinValueValidator(1, message="В жилье должна быть минимум 1 комната."),
            MaxValueValidator(20, message="Максимальное количество комнат — 20.")
        ]
    )

    housing_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=APARTMENT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title