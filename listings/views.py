from history.models import SearchHistory, ViewHistory
from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import models

from .models import Listing
from .serializers import ListingSerializer
from .filters import ListingFilter
from .permissions import IsLandlordOrReadOnly


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    # Кастомное правило доступа (Арендодатели создают/редактируют, остальные только читают)
    permission_classes = [IsLandlordOrReadOnly]

    # Подключение фильтрации, поиска и сортировки
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ListingFilter

    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user

        # Автоматическое сохранение истории поиска при наличии query-параметра 'search'
        search_query = self.request.query_params.get('search', None)
        if search_query:
            SearchHistory.objects.create(
                user=user if user.is_authenticated else None,
                query_text=search_query
            )

        # Разграничение видимости объявлений (анонимы видят только активные)
        if user.is_anonymous:
            return Listing.objects.filter(is_active=True)

        return Listing.objects.filter(models.Q(landlord=user) | models.Q(is_active=True)).distinct()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Автоматическое сохранение истории просмотров конкретного объявления
        ViewHistory.objects.create(
            user=request.user if request.user.is_authenticated else None,
            listing=instance
        )

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # Автоматически привязываем текущего авторизованного пользователя как хозяина жилья
        serializer.save(landlord=self.request.user)