from django_filters import rest_framework as filters
from .models import Listing


class ListingFilter(filters.FilterSet):
    # Фильтры для цены (минимальная и максимальная)
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    # Фильтры для количества комнат (диапазон)
    min_rooms = filters.NumberFilter(field_name="rooms", lookup_expr='gte')
    max_rooms = filters.NumberFilter(field_name="rooms", lookup_expr='lte')

    # Поиск по локации (город или район в Германии) без учета регистра
    location = filters.CharFilter(field_name="location", lookup_expr='icontains')

    class Meta:
        model = Listing
        fields = ['housing_type', 'is_active']