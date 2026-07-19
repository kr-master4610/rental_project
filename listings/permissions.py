from rest_framework import permissions

class IsLandlordOrReadOnly(permissions.BasePermission):
    """
    Permission to allow:
    - Safe methods (GET, HEAD, OPTIONS) for everyone.
    - Creation (POST) for authenticated users in the 'landlords' group.
    - Edit/Delete (PUT, PATCH, DELETE) only for the listing owner.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated and
            request.user.groups.filter(name='landlords').exists()
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.landlord == request.user