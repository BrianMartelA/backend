from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        # Verifica que el usuario esté autenticado y sea staff
        return request.user and request.user.is_authenticated and request.user.is_staff