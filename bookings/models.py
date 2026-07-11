from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from listings.models import Listing


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('rejected', 'Отклонено'),
        ('canceled', 'Отменено'),
    ]

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        # Проверяем даты только для новых бронирований
        if not self.pk and self.start_date < timezone.now().date():
            raise ValidationError("Дата начала бронирования не может быть в прошлом.")

        if self.start_date >= self.end_date:
            raise ValidationError("Дата окончания бронирования должна быть позже даты начала.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Бронь {self.tenant.email} ({self.status}) на {self.listing.title}"