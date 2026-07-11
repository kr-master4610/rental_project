from django.contrib import admin
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price', 'rooms', 'housing_type', 'is_active')
    search_fields = ('title', 'location')
