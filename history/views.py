from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from django.db.models.functions import Lower
from .models import SearchHistory, ViewHistory
from .serializers import SearchHistorySerializer, ViewHistorySerializer
from listings.models import Listing
from listings.serializers import ListingSerializer

class UserSearchHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve search history for the authenticated user.
    """
    serializer_class = SearchHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SearchHistory.objects.filter(user=self.request.user)

class UserViewHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve view history for the authenticated user.
    """
    serializer_class = ViewHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ViewHistory.objects.filter(user=self.request.user)

class PopularSearchesView(APIView):
    """
    Retrieve top popular search queries (case-insensitive aggregation).
    """
    def get(self, request):
        popular = (
            SearchHistory.objects.annotate(query_lower=Lower('query_text'))
            .values('query_lower')
            .annotate(count=Count('query_lower'))
            .order_by('-count')[:10]
        )
        # Transform results to match expected serializer/response keys format
        results = [{'query_text': item['query_lower'], 'count': item['count']} for item in popular]
        return Response(results, status=status.HTTP_200_OK)

class PopularListingsView(APIView):
    """
    Retrieve top viewed listings.
    """
    def get(self, request):
        popular_ids = (
            ViewHistory.objects.values('listing_id')
            .annotate(view_count=Count('listing_id'))
            .order_by('-view_count')[:10]
        )
        ids = [item['listing_id'] for item in popular_ids]
        listings = sorted(
            Listing.objects.filter(id__in=ids),
            key=lambda l: ids.index(l.id)
        )
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
