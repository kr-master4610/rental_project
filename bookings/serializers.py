from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.email')
    status = serializers.CharField(read_only=True)  # Явно указываем, что статус только для чтения

    class Meta:
        model = Booking
        fields = ['id', 'listing', 'tenant', 'start_date', 'end_date', 'status', 'created_at']

    def validate(self, data):
        # Проверяем базовое правило дат
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("Дата начала должна быть раньше даты окончания.")

        # Проверка овербукинга: ищем пересечения только с ПОДТВЕРЖДЕННЫМИ бронями
        overlapping_bookings = Booking.objects.filter(
            listing=data['listing'],
            status='confirmed',
            start_date__lte=data['end_date'],
            end_date__gte=data['start_date']
        )

        # Если мы обновляем существующую бронь, исключаем её саму из проверки
        if self.instance:
            overlapping_bookings = overlapping_bookings.exclude(pk=self.instance.pk)

        if overlapping_bookings.exists():
            raise serializers.ValidationError("Этот объект уже забронирован на указанные даты.")

        return data