from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model.
    """
    tenant = serializers.ReadOnlyField(source='tenant.email')
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'listing', 'tenant', 'start_date', 'end_date', 'status', 'created_at']

    def validate(self, data):
        """
        Validate booking dates and check for overlaps with confirmed bookings.
        """
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("Start date must be before end date.")

        # Check for overlaps only with confirmed bookings
        overlapping_bookings = Booking.objects.filter(
            listing=data['listing'],
            status='confirmed',
            start_date__lte=data['end_date'],
            end_date__gte=data['start_date']
        )

        if self.instance:
            overlapping_bookings = overlapping_bookings.exclude(pk=self.instance.pk)

        if overlapping_bookings.exists():
            raise serializers.ValidationError("This listing is already booked for these dates.")

        return data