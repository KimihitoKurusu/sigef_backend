from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from .helpers.permission_helpers import is_same_election_id


class IsCandidateManager(permissions.BasePermission):
    """
    Custom permission to only allow candidate managers to modify candidates.
    """

    def has_permission(self, request, view):
        # Verifica si el usuario autenticado pertenece al grupo de "Candidate Managers"
        election_id_from_data = request.data.get('election_id')
        election_id_from_url = view.kwargs.get('pk')
        user = request.user
        is_user_authenticated = user.is_authenticated
        is_candidate_manager = user.groups.filter(name='Candidate Managers').exists()
        user_election_id = user.election_id.id if is_user_authenticated and not isinstance(user,
                                                                                           AnonymousUser) else None

        return is_user_authenticated and is_candidate_manager and is_same_election_id(user_election_id,
                                                                                      election_id_from_data,
                                                                                      election_id_from_url, 'candidate')


class IsCandidateManagerOrReadOnly(IsCandidateManager):
    """
    Custom permission to allow read-only access to unauthenticated users
    and full access to candidate managers.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Permitir acceso de solo lectura para métodos seguros (GET, HEAD, OPTIONS)
            return True
        return super().has_permission(request, view)


class IsElectionManager(permissions.BasePermission):
    """
    Custom permission to only allow election managers to modify elections.
    """

    def has_permission(self, request, view):
        election_id_from_data = request.data.get('id')
        election_id_from_url = view.kwargs.get('pk')
        user = request.user
        is_user_authenticated = user.is_authenticated
        is_election_manager = user.groups.filter(name='Election Managers').exists()
        user_election_id = user.election_id.id if is_user_authenticated and not isinstance(user,
                                                                                           AnonymousUser) else None

        try:
            is_same_election_id(user_election_id, election_id_from_data, election_id_from_url, 'election')
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return is_user_authenticated and is_election_manager


class IsElectionManagerOrReadOnly(IsElectionManager):
    """
    Custom permission to allow read-only access to unauthenticated users
    and full access to election managers.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Permitir acceso de solo lectura para métodos seguros (GET, HEAD, OPTIONS)
            return True
        return super().has_permission(request, view)


class IsInstitutionManager(permissions.BasePermission):
    """
    Custom permission to only allow Superadmin managers to modify Institutions.
    """

    def has_permission(self, request, view):
        user = request.user
        is_user_authenticated = user.is_authenticated
        is_superuser = user.is_superuser
        return is_user_authenticated and is_superuser 


class IsInstitutionManagerOrReadOnly(IsInstitutionManager):
    """
    Custom permission to allow read-only access to unauthenticated users
    and full access to Superadmin.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Permitir acceso de solo lectura para métodos seguros (GET, HEAD, OPTIONS)
            return True
        return super().has_permission(request, view)

class IsCampusManager(permissions.BasePermission):
    """
    Custom permission to only allow Superadmin managers to modify Campuses.
    """

    def has_permission(self, request, view):
        user = request.user
        is_user_authenticated = user.is_authenticated
        is_superuser = user.is_superuser
        return is_user_authenticated and is_superuser 


class IsCampusManagerOrReadOnly(IsCampusManager):
    """
    Custom permission to allow read-only access to unauthenticated users
    and full access to Superadmin.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Permitir acceso de solo lectura para métodos seguros (GET, HEAD, OPTIONS)
            return True
        return super().has_permission(request, view)

class IsFacultyManager(permissions.BasePermission):
    """
    Custom permission to only allow Superadmin managers to modify Faculties.
    """

    def has_permission(self, request, view):
        user = request.user
        is_user_authenticated = user.is_authenticated
        is_superuser = user.is_superuser
        return is_user_authenticated and is_superuser 


class IsFacultyManagerOrReadOnly(IsFacultyManager):
    """
    Custom permission to allow read-only access to unauthenticated users
    and full access to Superadmin.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Permitir acceso de solo lectura para métodos seguros (GET, HEAD, OPTIONS)
            return True
        return super().has_permission(request, view)
