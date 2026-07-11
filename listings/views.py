from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Listing
from .serializers import ListingSerializer
from .filters import ListingFilter


# --- Управление объявлениями ---
class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ListingFilter

    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user

        # Если пользователь не авторизован — видит только активные объявления
        if user.is_anonymous:
            return Listing.objects.filter(is_active=True)

        # Авторизованный пользователь видит свои объявления (даже скрытые)
        # плюс все активные объявления от других пользователей
        return Listing.objects.filter(models.Q(landlord=user) | models.Q(is_active=True)).distinct()

    def perform_create(self, serializer):
        # Текущий пользователь автоматически становится арендодателем этого объекта
        serializer.save(landlord=self.request.user)