# permissions.py

from rest_framework.permissions import BasePermission

class IsHR(BasePermission):
    message = "Access denied. Only HR users can perform this action."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'HR'
        )