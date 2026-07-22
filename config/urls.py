from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views as auth_views
from listings.views import listing_list, create_listing, listing_detail
from users import views as user_views

urlpatterns = [
    # Main frontend entry point
    path('', listing_list, name='home'),
    path('property/<int:pk>/', listing_detail, name='listing_detail'),
    path('create/', create_listing, name='create_listing'),

    # Admin interface
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/users/', include('users.urls')),
    path('api/', include('listings.urls')),
    path('api/', include('bookings.urls')),
    path('api/', include('reviews.urls')),
    path('api/', include('history.urls')),

    # Authentication and documentation
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Web login/logout
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Registration
    path('register/', user_views.register, name='register'),

    # Password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]