from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminAuthorOrReadOnly(BasePermission):
    """Права у автора, админа или только чтение."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.is_superuser)


class IsAdminOrReadOnly(BasePermission):
    """Изменить контент может только админ."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin))
