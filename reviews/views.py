from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Review
from .serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Фильтруем отзывы, чтобы можно было легко получить отзывы конкретного объявления
    # Например: /api/reviews/?listing=1
    filterset_fields = ['listing']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)