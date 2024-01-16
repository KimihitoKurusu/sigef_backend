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
from elections.models import *


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


class CampusViewSetTest(TestCase):
   def setUp(self):
       self.client = APIClient()
       self.superadmin_user = get_user_model().objects.create_superuser(
           username='admin', password='adminpassword'
       )
       self.institution = Institution.objects.create(name='Test Institution')
       self.campus = Campus.objects.create(name='Test Campus', institution_id=self.institution)

   def test_list_campuses(self):
       response = self.client.get('/api/elections/campuses/')
       self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_retrieve_campus(self):
       response = self.client.get(f'/api/elections/campuses/{self.campus.id}/')
       self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_create_campus_as_superuser(self):
       self.client.force_authenticate(user=self.superadmin_user)
       data = {'name': 'New Campus', 'institution_id': self.institution.id}
       response = self.client.post('/api/elections/campuses/', data)
       self.assertEqual(response.status_code, status.HTTP_201_CREATED)

   def test_create_campus_as_regular_user(self):
       regular_user = get_user_model().objects.create_user(
           username='user', password='userpassword'
       )
       self.client.force_authenticate(user=regular_user)
       data = {'name': 'New Campus', 'institution_id': self.institution.id}
       response = self.client.post('/api/elections/campuses/', data)
       self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

   def test_update_campus_as_superuser(self):
       self.client.force_authenticate(user=self.superadmin_user)
       data = {'name': 'Updated Campus', 'institution_id': self.institution.id}
       response = self.client.put(f'/api/elections/campuses/{self.campus.id}/', data)
       self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_update_campus_as_regular_user(self):
       regular_user = get_user_model().objects.create_user(
           username='user', password='userpassword'
       )
       self.client.force_authenticate(user=regular_user)
       data = {'name': 'Updated Campus', 'institution_id': self.institution.id}
       response = self.client.put(f'/api/elections/campuses/{self.campus.id}/', data)
       self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

   def test_delete_campus_as_superuser(self):
       self.client.force_authenticate(user=self.superadmin_user)
       response = self.client.delete(f'/api/elections/campuses/{self.campus.id}/')
       self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

   def test_delete_campus_as_regular_user(self):
       regular_user = get_user_model().objects.create_user(
           username='user', password='userpassword'
       )
       self.client.force_authenticate(user=regular_user)
       response = self.client.delete(f'/api/elections/campuses/{self.campus.id}/')
       self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class FacultyViewSetTest(TestCase):
  def setUp(self):
      self.client = APIClient()
      self.superadmin_user = get_user_model().objects.create_superuser(
          username='admin', password='adminpassword'
      )
      self.institution = Institution.objects.create(name='Test Institution')
      self.campus = Campus.objects.create(name='Test Campus', institution_id=self.institution)
      self.faculty = Faculty.objects.create(name='Test Faculty', campus_id=self.campus)

  def test_list_faculties(self):
      response = self.client.get('/api/elections/faculties/')
      self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_retrieve_faculty(self):
      response = self.client.get(f'/api/elections/faculties/{self.faculty.id}/')
      self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_create_faculty_as_superuser(self):
      self.client.force_authenticate(user=self.superadmin_user)
      data = {'name': 'New Faculty', 'campus_id': self.campus.id}
      response = self.client.post('/api/elections/faculties/', data)
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)

  def test_create_faculty_as_regular_user(self):
      regular_user = get_user_model().objects.create_user(
          username='user', password='userpassword'
      )
      self.client.force_authenticate(user=regular_user)
      data = {'name': 'New Faculty', 'campus_id': self.campus.id}
      response = self.client.post('/api/elections/faculties/', data)
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

  def test_update_faculty_as_superuser(self):
      self.client.force_authenticate(user=self.superadmin_user)
      data = {'name': 'Updated Faculty', 'campus_id': self.campus.id}
      response = self.client.put(f'/api/elections/faculties/{self.faculty.id}/', data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_update_faculty_as_regular_user(self):
      regular_user = get_user_model().objects.create_user(
          username='user', password='userpassword'
      )
      self.client.force_authenticate(user=regular_user)
      data = {'name': 'Updated Faculty', 'campus_id': self.campus.id}
      response = self.client.put(f'/api/elections/faculties/{self.faculty.id}/', data)
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

  def test_delete_faculty_as_superuser(self):
      self.client.force_authenticate(user=self.superadmin_user)
      response = self.client.delete(f'/api/elections/faculties/{self.faculty.id}/')
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

  def test_delete_faculty_as_regular_user(self):
      regular_user = get_user_model().objects.create_user(
          username='user', password='userpassword'
      )
      self.client.force_authenticate(user=regular_user)
      response = self.client.delete(f'/api/elections/faculties/{self.faculty.id}/')
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PersonViewSetTest(TestCase):
 def setUp(self):
     self.client = APIClient()
     self.url = '/api/elections/people/'
     self.superadmin_user = get_user_model().objects.create_superuser(
         username='admin', password='adminpassword'
     )
     self.institution = Institution.objects.create(name='Test Institution')
     self.campus = Campus.objects.create(name='Test Campus', institution_id=self.institution)
     self.faculty = Faculty.objects.create(name='Test Faculty', campus_id=self.campus)
     self.person = Person.objects.create(ci='12345678901', name='Test', last_name='Person', faculty_id=self.faculty)

 def test_list_persons(self):
     response = self.client.get(self.url)
     self.assertEqual(response.status_code, status.HTTP_200_OK)

 def test_retrieve_person(self):
     response = self.client.get(f'{self.url}{self.person.ci}/')
     self.assertEqual(response.status_code, status.HTTP_200_OK)

 def test_create_person_as_superuser(self):
     self.client.force_authenticate(user=self.superadmin_user)
     data = {'ci': '12345678902', 'name': 'New', 'last_name': 'Person', 'faculty_id': self.faculty.id}
     response = self.client.post(self.url, data)
     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

 def test_create_person_as_regular_user(self):
     regular_user = get_user_model().objects.create_user(
         username='user', password='userpassword'
     )
     self.client.force_authenticate(user=regular_user)
     data = {'ci': '12345678902', 'name': 'New', 'last_name': 'Person', 'faculty_id': self.faculty.id}
     response = self.client.post(self.url, data)
     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

 def test_update_person_as_superuser(self):
     self.client.force_authenticate(user=self.superadmin_user)
     data = {'name': 'Updated', 'last_name': 'Person', 'faculty_id': self.faculty.id}
     response = self.client.put(f'{self.url}{self.person.ci}/', data)
     print('fherwivgnhgvjoirewzhgvieroanhe', response)
     self.assertEqual(response.status_code, status.HTTP_200_OK)

 def test_update_person_as_regular_user(self):
     regular_user = get_user_model().objects.create_user(
         username='user', password='userpassword'
     )
     self.client.force_authenticate(user=regular_user)
     data = {'name': 'Updated', 'last_name': 'Person', 'faculty_id': self.faculty.id}
     response = self.client.put(f'{self.url}{self.person.ci}/', data)
     # self.assertEqual(response.status_code, status.HTTP_200_OK)
     r =self.client.get(f'{self.url}{self.person.ci}')
     print(r)
     self.assertEqual(self.person.ci, r.body.get('ci'))

 def test_delete_person_as_superuser(self):
     self.client.force_authenticate(user=self.superadmin_user)
     response = self.client.delete(f'{self.url}{self.person.ci}/')
     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

 def test_delete_person_as_regular_user(self):
     regular_user = get_user_model().objects.create_user( username='user', password='userpassword' ) 
     self.client.force_authenticate(user=regular_user) 
     response = self.client.delete(f'{self.url}{self.person.ci}/') 
     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ElectionViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superadmin_user = get_user_model().objects.create_superuser(
            username='admin', password='adminpassword'
        )
        self.election = Election.objects.create(name='Test Election')

    def test_list_elections(self):
        response = self.client.get('/api/elections/elections/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_election(self):
        response = self.client.get(f'/api/elections/elections/{self.election.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_election_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        data = {'name': 'New Election'}
        response = self.client.post('/api/elections/elections/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_election_as_regular_user(self):
        regular_user = get_user_model().objects.create_user(
            username='user', password='userpassword'
        )
        self.client.force_authenticate(user=regular_user)
        data = {'name': 'New Election'}
        response = self.client.post('/api/elections/elections/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_election_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        data = {'name': 'Updated Election'}
        response = self.client.put(f'/api/elections/elections/{self.election.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_election_as_regular_user(self):
        regular_user = get_user_model().objects.create_user(
            username='user', password='userpassword'
        )
        self.client.force_authenticate(user=regular_user)
        data = {'name': 'Updated Election'}
        response = self.client.put(f'/api/elections/elections/{self.election.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_election_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        response = self.client.delete(f'/api/elections/elections/{self.election.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_election_as_regular_user(self):
        regular_user = get_user_model().objects.create_user(
            username='user', password='userpassword'
        )
        self.client.force_authenticate(user=regular_user)
        response = self.client.delete(f'/api/elections/elections/{self.election.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CandidateViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superadmin_user = get_user_model().objects.create_superuser(
            username='admin', password='adminpassword'
        )
        self.candidate = Institution.objects.create(name='Test Institution')

    def test_list_candidates(self):
        response = self.client.get('/api/elections/candidates/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_candidate(self):
        response = self.client.get(f'/api/elections/candidates/{self.candidate.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_candidate_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        data = {'name': 'New Institution'}
        response = self.client.post('/api/elections/candidates/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_candidate_as_regular_user(self):
        regular_user = get_user_model().objects.create_user(
            username='user', password='userpassword'
        )
        self.client.force_authenticate(user=regular_user)
        data = {'name': 'New Institution'}
        response = self.client.post('/api/elections/candidates/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_candidate_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        data = {'name': 'Updated Institution'}
        response = self.client.put(f'/api/elections/candidates/{self.candidate.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_candidate_as_regular_user(self):
        regular_user = get_user_model().objects.create_user(
            username='user', password='userpassword'
        )
        self.client.force_authenticate(user=regular_user)
        data = {'name': 'Updated Institution'}
        response = self.client.put(f'/api/elections/candidates/{self.candidate.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_candidate_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        response = self.client.delete(f'/api/elections/candidates/{self.candidate.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_candidate_as_regular_user(self):
        regular_user = get_user_model().objects.create_user(
            username='user', password='userpassword'
        )
        self.client.force_authenticate(user=regular_user)
        response = self.client.delete(f'/api/elections/candidates/{self.candidate.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ElectorRegistryViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superadmin_user = get_user_model().objects.create_superuser(
            username='admin', password='adminpassword'
        )
        self.elector_registry = Institution.objects.create(name='Test Institution')

    def test_list_elector_registries(self):
        response = self.client.get('/api/elections/elector-registries/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_elector_registry(self):
        response = self.client.get(f'/api/elections/elector-registries/{self.elector_registry.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_elector_registry_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        data = {'name': 'New Institution'}
        response = self.client.post('/api/elections/elector-registries/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_elector_registry_as_regular_user(self):
        regular_user = get_user_model().objects.create_user(
            username='user', password='userpassword'
        )
        self.client.force_authenticate(user=regular_user)
        data = {'name': 'New Institution'}
        response = self.client.post('/api/elections/elector-registries/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_elector_registry_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        data = {'name': 'Updated Institution'}
        response = self.client.put(f'/api/elections/elector-registries/{self.elector_registry.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_elector_registry_as_regular_user(self):
        regular_user = get_user_model().objects.create_user(
            username='user', password='userpassword'
        )
        self.client.force_authenticate(user=regular_user)
        data = {'name': 'Updated Institution'}
        response = self.client.put(f'/api/elections/elector-registries/{self.elector_registry.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_elector_registry_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        response = self.client.delete(f'/api/elections/elector-registries/{self.elector_registry.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_elector_registry_as_regular_user(self):
        regular_user = get_user_model().objects.create_user(
            username='user', password='userpassword'
        )
        self.client.force_authenticate(user=regular_user)
        response = self.client.delete(f'/api/elections/elector-registries/{self.elector_registry.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

