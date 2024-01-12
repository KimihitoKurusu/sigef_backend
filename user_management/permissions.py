from rest_framework import permissions


class IsUserManager(permissions.BasePermission):
    """
    Custom permission to only allow candidate managers to modify candidates.
    """

    def has_permission(self, request, view):
        user = request.user
        is_user_authenticated = user.is_authenticated
        is_superuser = user.is_superuser
        if is_user_authenticated:
            is_current_user = user.ci == request.data.get('ci') or user.ci == view.kwargs.get('pk')
            return is_superuser or is_current_user
        return False
