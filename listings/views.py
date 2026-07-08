from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
from .permissions import IsLandlordOrReadOnly
from .filters import ListingFilter

# --- Управление объявлениями ---
class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsLandlordOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ListingFilter

    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        # Анонимы и Арендаторы видят только активные объявления
        if user.is_anonymous or user.role == 'tenant':
            return Listing.objects.filter(is_active=True)

        # Арендодатели видят свои объявления
        return Listing.objects.filter(landlord=user)

    def perform_create(self, serializer):
        serializer.save(landlord=self.request.user)


# --- Управление бронированиями ---
class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Арендодатель видит бронирования только на свои квартиры
        if user.role == 'landlord':
            return Booking.objects.filter(listing__landlord=user)
        # Арендатор видит только свои бронирования
        return Booking.objects.filter(tenant=user)

    def perform_create(self, serializer):
        # Автоматически подставляем текущего юзера как арендатора
        serializer.save(tenant=self.request.user)