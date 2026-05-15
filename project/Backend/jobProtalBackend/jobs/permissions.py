# permissions.py

from rest_framework.permissions import BasePermission

class IsHR(BasePermission):
    message = "Access denied. Only HR users can perform this action."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'HR'
        )


class IsSeeker(BasePermission):
    """Permission class for job seekers"""
    message = "Access denied. Only Seeker users can perform this action."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'SEEKER'
        )


class IsAdmin(BasePermission):
    """Permission class for admin users"""
    message = "Access denied. Only Admin users can perform this action."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'ADMIN'
        )


class IsModeratorOrAdmin(BasePermission):
    """Permission class for moderators or admin users"""
    message = "Access denied. Only Moderators or Admin users can perform this action."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.role == 'ADMIN' or request.user.is_moderator)
        )


class IsOwnerOrAdmin(BasePermission):
    """Permission to check if user is the owner or admin"""
    message = "Access denied. You don't have permission to perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow admin to access anything
        if request.user.role == 'ADMIN':
            return True
        # Allow object owner to access
        if hasattr(obj, 'user') and obj.user == request.user:
            return True
        if hasattr(obj, 'owner') and obj.owner == request.user:
            return True
        return False


class CanReportJob(BasePermission):
    """Permission to check if user can report a job"""
    message = "Only seekers can report jobs."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'SEEKER'
        )


class CanManageReports(BasePermission):
    """Permission to check if user can manage reports"""
    message = "Only moderators or admins can manage reports."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.role == 'ADMIN' or request.user.is_moderator)
        )
