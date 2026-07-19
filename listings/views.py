from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .models import Listing
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from .serializers import ListingSerializer
from .filters import ListingFilter
from .permissions import IsLandlordOrReadOnly
from history.models import SearchHistory, ViewHistory
from rest_framework.response import Response

from listings.forms import ListingForm

def listing_list(request):
    # Fetch only active listings to display on the frontend
    listings = Listing.objects.filter(is_active=True)
    return render(request, 'listings/list.html', {'listings': listings})

@login_required
def create_listing(request):
    # Handle listing creation for authenticated users
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.landlord = request.user
            listing.save()
            return redirect('home')
    else:
        form = ListingForm()
    return render(request, 'listings/create.html', {'form': form})

class ListingViewSet(viewsets.ModelViewSet):

    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsLandlordOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ListingFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        search_query = self.request.query_params.get('search', None)

        if search_query:
            SearchHistory.objects.create(
                user=user if user.is_authenticated else None,
                query_text=search_query
            )

        if user.is_anonymous:
            return Listing.objects.filter(is_active=True)

        return Listing.objects.filter(models.Q(landlord=user) | models.Q(is_active=True)).distinct()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        ViewHistory.objects.create(
            user=request.user if request.user.is_authenticated else None,
            listing=instance
        )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(landlord=self.request.user)