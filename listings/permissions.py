from rest_framework import permissions


class IsLandlordOrReadOnly(permissions.BasePermission):
    """
    Разрешение:
    - Читать (GET, HEAD, OPTIONS) разрешено кому угодно.
    - Создавать (POST) могут только авторизованные пользователи из группы 'landlords'.
    - Редактировать или удалять (PUT, PATCH, DELETE) — только сам хозяин этого объявления.
    """
    def has_permission(self, request, view):
        # Читать разрешено всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Проверяем, авторизован ли пользователь и состоит ли он в группе 'landlords'
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name='landlords').exists()
        )

    def has_object_permission(self, request, view, obj):
        # Смотреть конкретное объявление могут все
        if request.method in permissions.SAFE_METHODS:
            return True

        # Редактировать или удалять — только сам хозяин этого объявления
        return obj.landlord == request.user