from django_filters import rest_framework as filters
from .models import Listing

class ListingFilter(filters.FilterSet):
    # Фильтрация по диапазону цен (минимальная и максимальная)
    price_min = filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = filters.NumberFilter(field_name="price", lookup_expr='lte')

    # Фильтрация по диапазону комнат
    rooms_min = filters.NumberFilter(field_name="rooms", lookup_expr='gte')
    rooms_max = filters.NumberFilter(field_name="rooms", lookup_expr='lte')

    # Поиск по городу/району (без учета регистра)
    location = filters.CharFilter(field_name="location", lookup_expr='icontains')

    class Meta:
        model = Listing
        fields = ['housing_type', 'location']