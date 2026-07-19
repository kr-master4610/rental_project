from rest_framework import serializers
from .models import Review
from bookings.models import Booking

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.
    """
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Review
        fields = ['id', 'listing', 'author', 'rating', 'text', 'created_at']

    def validate(self, data):
        user = self.context['request'].user
        listing = data['listing']

        # Validate that the user has a confirmed booking for this listing
        has_booked = Booking.objects.filter(
            tenant=user,
            listing=listing,
            status='confirmed'
        ).exists()

        if not has_booked:
            raise serializers.ValidationError(
                "You cannot leave a review without a confirmed booking."
            )

        # Protection: only one review per user per listing
        if Review.objects.filter(author=user, listing=listing).exists():
            raise serializers.ValidationError(
                "You have already left a review for this listing."
            )

        return data