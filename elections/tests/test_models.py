import json
import unittest
from unittest.mock import MagicMock

import jwt
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from elections.helpers.permission_helpers import verification_token
from elections.models import Institution
from elections.permissions import IsInstitutionManagerOrReadOnly


class VerificarTokenTest(unittest.TestCase):

    def assertJsonResponseEqual(self, response, expected_status, expected_data):
        self.assertEqual(response.status_code, expected_status)
        self.assertEqual(json.loads(response.content), expected_data)

    def test_verificar_token_exitoso(self):
        # Simula una solicitud HTTP con un encabezado de autorización válido
        request = MagicMock()
        request.headers.get.return_value = 'tu_token_valido'

        # Simula el comportamiento esperado de jwt.decode para un token válido
        with unittest.mock.patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {'info': 'data'}

            # Llama a la función y verifica que devuelva el payload correctamente
            result = verification_token(request)
            self.assertEqual(result, {'info': 'data'})

            # Verifica que la función se llamó correctamente con los parámetros esperados
            mock_decode.assert_called_once_with('tu_token_valido', 'tu_clave_secreta', algorithms=['HS256'])

    def test_verificar_token_expirado(self):
        # Simula una solicitud HTTP con un encabezado de autorización válido
        request = MagicMock()
        request.headers.get.return_value = 'tu_token_expirado'

        # Simula el comportamiento esperado de jwt.decode para un token con firma expirada
        with unittest.mock.patch('jwt.decode') as mock_decode:
            mock_decode.side_effect = jwt.ExpiredSignatureError('Token expirado')

            # Llama a la función y verifica que devuelva un JsonResponse con el error correspondiente
            result = verification_token(request)
            expected_response = JsonResponse({'error': 'Token expirado'}, status=401)
            self.assertJsonResponseEqual(result, expected_response.status_code, json.loads(expected_response.content))

    def test_verificar_token_invalido(self):
        # Simula una solicitud HTTP con un encabezado de autorización válido
        request = MagicMock()
        request.headers.get.return_value = 'tu_token_invalido'

        # Simula el comportamiento esperado de jwt.decode para un token inválido
        with unittest.mock.patch('jwt.decode') as mock_decode:
            mock_decode.side_effect = jwt.InvalidTokenError('Token inválido')

            # Llama a la función y verifica que devuelva un JsonResponse con el error correspondiente
            result = verification_token(request)
            expected_response = JsonResponse({'error': 'Token inválido'}, status=401)
            self.assertJsonResponseEqual(result, expected_response.status_code, json.loads(expected_response.content))


class InstitutionViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superadmin_user = get_user_model().objects.create_superuser(
            username='admin', password='adminpassword'
        )
        self.institution = Institution.objects.create(name='Test Institution')

    def test_list_institutions(self):
        response = self.client.get('/api/elections/institutions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_institution(self):
        response = self.client.get(f'/api/elections/institutions/{self.institution.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_institution_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        data = {'name': 'New Institution'}
        response = self.client.post('/api/elections/institutions/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_institution_as_regular_user(self):
        regular_user = get_user_model().objects.create_user(
            username='user', password='userpassword'
        )
        self.client.force_authenticate(user=regular_user)
        data = {'name': 'New Institution'}
        response = self.client.post('/api/elections/institutions/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_institution_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        data = {'name': 'Updated Institution'}
        response = self.client.put(f'/api/elections/institutions/{self.institution.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_institution_as_regular_user(self):
        regular_user = get_user_model().objects.create_user(
            username='user', password='userpassword'
        )
        self.client.force_authenticate(user=regular_user)
        data = {'name': 'Updated Institution'}
        response = self.client.put(f'/api/elections/institutions/{self.institution.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_institution_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        response = self.client.delete(f'/api/elections/institutions/{self.institution.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_institution_as_regular_user(self):
        regular_user = get_user_model().objects.create_user(
            username='user', password='userpassword'
        )
        self.client.force_authenticate(user=regular_user)
        response = self.client.delete(f'/api/elections/institutions/{self.institution.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class IsInstitutionManagerOrReadOnlyTest(TestCase):
    def setUp(self):
        self.permission = IsInstitutionManagerOrReadOnly()
        self.user = get_user_model().objects.create_user(
            username='user', password='userpassword'
        )
        self.superadmin_user = get_user_model().objects.create_superuser(
            username='admin', password='adminpassword'
        )
        self.institution = Institution.objects.create(name='Test Institution')

    def _create_request(self, method, user=None):
        response = None
        client = APIClient()
        if user:
            client.force_authenticate(user=user)

        url = '/api/elections/institutions/'  # Replace 'some-url-name' with the actual URL name
        if method == 'GET':
            response = client.get(url)
        elif method == 'POST':
            response = client.post(url, data={})
        elif method == 'HEAD':
            response = client.head(url)
        elif method == 'OPTIONS':
            response = client.options(url)
        # Add more cases for other HTTP methods as needed
        return response

    def test_read_permission(self):
        response = self._create_request('GET', user=self.user)
        self.assertTrue(self.permission.has_permission(response.wsgi_request, None))

    def test_safe_methods_read_permission(self):
        safe_methods = ['GET', 'HEAD', 'OPTIONS']
        for method in safe_methods:
            response = self._create_request(method, user=self.user)
            self.assertTrue(self.permission.has_permission(response.wsgi_request, None))

    def test_write_permission_as_regular_user(self):
        response = self._create_request('POST', user=self.user)
        self.assertFalse(self.permission.has_permission(response.wsgi_request, None))

    def test_write_permission_as_superuser(self):
        response = self._create_request('POST', user=self.superadmin_user)
        self.assertTrue(self.permission.has_permission(response.wsgi_request, None))


