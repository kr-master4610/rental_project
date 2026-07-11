from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.email')

    class Meta:
        model = Booking
        fields = ['id', 'listing', 'tenant', 'start_date', 'end_date', 'created_at']

    def validate(self, data):
        # Проверяем базовое правило дат (на всякий случай удваиваем логику модели)
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("Дата начала должна быть раньше даты окончания.")

        # Проверка овербукинга: бронирование одного объекта разными людьми на одно время
        overlapping_bookings = Booking.objects.filter(
            listing=data['listing'],
            start_date__lte=data['end_date'],
            end_date__gte=data['start_date']
        )

        # Если мы обновляем бронь, исключаем её саму из проверки
        if self.instance:
            overlapping_bookings = overlapping_bookings.exclude(pk=self.instance.pk)

        if overlapping_bookings.exists():
            raise serializers.ValidationError("Этот объект уже забронирован на указанные даты.")

        return data