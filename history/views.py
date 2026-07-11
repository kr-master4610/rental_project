from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from .models import SearchHistory, ViewHistory
from .serializers import SearchHistorySerializer, ViewHistorySerializer
from listings.models import Listing
from listings.serializers import ListingSerializer


class UserSearchHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод истории поиска текущего пользователя"""
    serializer_class = SearchHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SearchHistory.objects.filter(user=self.request.user)


class UserViewHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод истории просмотров объявлений текущего пользователя"""
    serializer_class = ViewHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ViewHistory.objects.filter(user=self.request.user)


class PopularSearchesView(APIView):
    """Топ-популярных поисковых запросов во всем сервисе"""

    def get(self, request):
        popular = (
            SearchHistory.objects.values('query_text')
            .annotate(count=Count('query_text'))
            .order_by('-count')[:10]
        )
        return Response(popular, status=status.HTTP_200_OK)


class PopularListingsView(APIView):
    """Топ-просматриваемых объявлений недвижимости"""

    def get(self, request):
        # Находим ID самых просматриваемых объявлений
        popular_ids = (
            ViewHistory.objects.values('listing_id')
            .annotate(view_count=Count('listing_id'))
            .order_by('-view_count')[:10]
        )

        # Вытаскиваем сами объекты объявлений
        ids = [item['listing_id'] for item in popular_ids]
        # Сохраняем порядок сортировки по популярности
        listings = sorted(
            Listing.objects.filter(id__in=ids),
            key=lambda l: ids.index(l.id)
        )

        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
