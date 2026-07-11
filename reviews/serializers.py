from rest_framework import serializers
from .models import Review
from bookings.models import Booking

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Review
        fields = ['id', 'listing', 'author', 'rating', 'text', 'created_at']

    def validate(self, data):
        user = self.context['request'].user
        listing = data['listing']

        # Проверяем, бронировал ли этот пользователь данное жилье со статусом 'confirmed'
        has_booked = Booking.objects.filter(
            tenant=user,
            listing=listing,
            status='confirmed'
        ).exists()

        if not has_booked:
            raise serializers.ValidationError(
                "Вы не можете оставить отзыв, так как у вас нет подтвержденных бронирований этого жилья."
            )

        # Защита: один пользователь — один отзыв на конкретное объявление
        if Review.objects.filter(author=user, listing=listing).exists():
            raise serializers.ValidationError(
                "Вы уже оставили отзыв для этого объявления."
            )

        return data