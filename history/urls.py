from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserSearchHistoryViewSet,
    UserViewHistoryViewSet,
    PopularSearchesView,
    PopularListingsView
)

router = DefaultRouter()
router.register(r'history/searches', UserSearchHistoryViewSet, basename='user-searches')
router.register(r'history/views', UserViewHistoryViewSet, basename='user-views')

urlpatterns = [
    path('', include(router.urls)),
    path('popular/searches/', PopularSearchesView.as_view(), name='popular-searches'),
    path('popular/listings/', PopularListingsView.as_view(), name='popular-listings'),
]