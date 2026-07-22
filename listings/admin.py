from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Listing

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price', 'rooms', 'housing_type', 'is_active')
    search_fields = ('title', 'location')
