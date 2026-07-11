from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Если пользователь из группы landlords, он видит запросы на свои объекты
        if user.groups.filter(name='landlords').exists():
            return Booking.objects.filter(listing__landlord=user)
        # Арендаторы видят только то, что забронировали сами
        return Booking.objects.filter(tenant=user)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)

    # 1. Подтверждение брони (Доступно только хозяину объявления)
    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        booking = self.get_object()
        if booking.listing.landlord != request.user:
            return Response({"error": "Вы не являетесь хозяином этого жилья."}, status=status.HTTP_403_FORBIDDEN)

        booking.status = 'confirmed'
        booking.save()
        return Response({"status": "Бронирование успешно подтверждено."}, status=status.HTTP_200_OK)

    # 2. Отклонение брони (Доступно только хозяину объявления)
    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        booking = self.get_object()
        if booking.listing.landlord != request.user:
            return Response({"error": "Вы не являетесь хозяином этого жилья."}, status=status.HTTP_403_FORBIDDEN)

        booking.status = 'rejected'
        booking.save()
        return Response({"status": "Бронирование отклонено."}, status=status.HTTP_200_OK)

    # 3. Отмена брони (Доступно арендатору до даты начала)
    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        # Арендатор отменяет свою бронь
        booking = Booking.objects.filter(tenant=request.user, pk=pk).first()
        if not booking:
            return Response({"error": "Бронирование не найдено среди ваших заказов."}, status=status.HTTP_404_NOT_FOUND)

        if booking.start_date <= timezone.now().date():
            return Response({"error": "Нельзя отменить бронирование, которое уже началось или прошло."},
                            status=status.HTTP_400_BAD_REQUEST)

        booking.status = 'canceled'
        booking.save()
        return Response({"status": "Бронирование успешно отменено."}, status=status.HTTP_200_OK)