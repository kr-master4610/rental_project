from rest_framework import serializers
from .models import SearchHistory, ViewHistory
from listings.serializers import ListingSerializer

class SearchHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for search history.
    """
    class Meta:
        model = SearchHistory
        fields = ['id', 'query_text', 'created_at']

class ViewHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for view history with listing details.
    """
    listing = ListingSerializer(read_only=True)

    class Meta:
        model = ViewHistory
        fields = ['id', 'listing', 'viewed_at']