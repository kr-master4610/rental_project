from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/', include('listings.urls')),
    # Вот эта строчка включит вход для интерфейса DRF:
    path('api-auth/', include('rest_framework.urls')),
]