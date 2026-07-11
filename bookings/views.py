from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Каждый пользователь (роль теперь общая) видит свои бронирования
        return Booking.objects.filter(tenant=self.request.user)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)
