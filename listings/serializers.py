from rest_framework import serializers
from .models import Listing

class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Listing model.
    """
    landlord = serializers.ReadOnlyField(source='landlord.email')

    class Meta:
        model = Listing
        fields = [
            'id', 'landlord', 'title', 'description',
            'location', 'price', 'rooms', 'housing_type',
            'is_active', 'created_at'
        ]