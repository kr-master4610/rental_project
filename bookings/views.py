from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling booking actions.
    """
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter bookings based on user role.
        """
        user = self.request.user
        if user.groups.filter(name='landlords').exists():
            return Booking.objects.filter(listing__landlord=user)
        return Booking.objects.filter(tenant=user)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        """
        Approve a booking. Restricted to the listing landlord.
        """
        booking = self.get_object()
        if booking.listing.landlord != request.user:
            return Response({"error": "You are not the landlord of this listing."},
                            status=status.HTTP_403_FORBIDDEN)

        booking.status = 'confirmed'
        booking.save()
        return Response({"status": "Booking confirmed successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        """
        Reject a booking. Restricted to the listing landlord.
        """
        booking = self.get_object()
        if booking.listing.landlord != request.user:
            return Response({"error": "You are not the landlord of this listing."},
                            status=status.HTTP_403_FORBIDDEN)

        booking.status = 'cancelled'  # Standardized to 'cancelled'
        booking.save()
        return Response({"status": "Booking rejected."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        """
        Cancel a booking. Available to the tenant before the start date.
        """
        booking = Booking.objects.filter(tenant=request.user, pk=pk).first()
        if not booking:
            return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

        if booking.start_date <= timezone.now().date():
            return Response({"error": "Cannot cancel a booking that has already started or passed."},
                            status=status.HTTP_400_BAD_REQUEST)

        booking.status = 'cancelled'
        booking.save()
        return Response({"status": "Booking cancelled successfully."}, status=status.HTTP_200_OK)