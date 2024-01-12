from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from user_management.models import CustomUser


class IsUserManager(permissions.BasePermission):
    """
    Custom permission to only allow candidate managers to modify candidates.
    """

    def has_permission(self, request, view):
        user = request.user
        is_user_authenticated = user.is_authenticated
        is_superuser = user.is_superuser
        is_current_user = user.ci == request.body.ci or user.ci == view.kwargs.get('pk')
        return is_user_authenticated and (is_superuser or is_current_user) 