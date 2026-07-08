from rest_framework import permissions


class IsLandlordOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Читать (GET, HEAD, OPTIONS) разрешено кому угодно
        if request.method in permissions.SAFE_METHODS:
            return True

        # Изменять данные может только авторизованный пользователь с ролью landlord
        return request.user.is_authenticated and request.user.role == 'landlord'

    def has_object_permission(self, request, view, obj):
        # Смотреть конкретное объявление могут все
        if request.method in permissions.SAFE_METHODS:
            return True

        # Редактировать или удалять — только сам хозяин этого объявления
        return obj.landlord == request.user