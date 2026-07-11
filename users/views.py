from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Генерируем JWT-токены для только что зарегистрированного пользователя
            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "Пользователь успешно зарегистрирован!",
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    Эндпоинт для получения данных о текущем авторизованном пользователе.
    Помогает узнать, в какой группе (роли) находится юзер.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Выясняем роли на основе групп Django
        groups = list(user.groups.values_list('name', flat=True))

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "roles": groups
        }, status=status.HTTP_200_OK)