from rest_framework import serializers
from .models import Listing
from .models import Booking

class ListingSerializer(serializers.ModelSerializer):
    landlord = serializers.ReadOnlyField(source='landlord.email')

    class Meta:
        model = Listing
        fields = [
            'id', 'landlord', 'title', 'description',
            'location', 'price', 'rooms', 'housing_type',
            'is_active', 'created_at'
        ]
from .models import Listing, Booking  # Обновили импорт

class BookingSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.email')

    class Meta:
        model = Booking
        fields = ['id', 'listing', 'tenant', 'start_date', 'end_date', 'created_at']

    def validate(self, data):
        # Проверяем, что дата начала раньше даты конца
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("Дата начала должна быть раньше даты окончания бронирования.")

        # Главная магия: ищем пересечения диапазонов в базе данных
        # Формула пересечения: (StartA <= EndB) AND (EndA >= StartB)
        overlapping_bookings = Booking.objects.filter(
            listing=data['listing'],
            start_date__lte=data['end_date'],
            end_date__gte=data['start_date']
        )

        if overlapping_bookings.exists():
            raise serializers.ValidationError("К сожалению, эти даты уже заняты другим бронированием.")

        return data