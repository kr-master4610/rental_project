from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserProfileView

urlpatterns = [
    # Регистрация нового пользователя (возвращает данные и JWT-токены)
    path('register/', RegisterView.as_view(), name='register'),

    # Вход (Получение JWT access и refresh токенов по username и password)
    path('login/', TokenObtainPairView.as_view(), name='login'),

    # Обновление протухшего access-токена с помощью refresh-токена
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Профиль текущего авторизованного пользователя (показывает его группы/роли)
    path('me/', UserProfileView.as_view(), name='user_profile'),
]