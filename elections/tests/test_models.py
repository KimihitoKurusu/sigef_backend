import json
import unittest
from datetime import timedelta
from unittest.mock import MagicMock

import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from elections.helpers.permission_helpers import verification_token
from elections.models import *
from .factory.models_factory import *
from ..serializers import ElectorRegistrySerializer


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
        self.institution = InstitutionFactory()
        self.regular_user = get_user_model().objects.create_user(
            username='user', password='userpassword', person=PersonFactory()
        )

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
        self.client.force_authenticate(user=self.regular_user)
        data = {'name': 'New Institution'}
        response = self.client.post('/api/elections/institutions/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_institution_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        data = {'name': 'Updated Institution'}
        response = self.client.put(f'/api/elections/institutions/{self.institution.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_institution_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {'name': 'Updated Institution'}
        response = self.client.put(f'/api/elections/institutions/{self.institution.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_institution_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        response = self.client.delete(f'/api/elections/institutions/{self.institution.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_institution_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(f'/api/elections/institutions/{self.institution.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CampusViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superadmin_user = get_user_model().objects.create_superuser(
            username='admin', password='adminpassword'
        )
        self.institution = InstitutionFactory()
        self.campus = CampusFactory()
        self.regular_user = get_user_model().objects.create_user(
            username='user', password='userpassword', person=PersonFactory()
        )

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
        self.client.force_authenticate(user=self.regular_user)
        data = {'name': 'New Campus', 'institution_id': self.institution.id}
        response = self.client.post('/api/elections/campuses/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_campus_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        data = {'name': 'Updated Campus', 'institution_id': self.institution.id}
        response = self.client.put(f'/api/elections/campuses/{self.campus.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_campus_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {'name': 'Updated Campus', 'institution_id': self.institution.id}
        response = self.client.put(f'/api/elections/campuses/{self.campus.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_campus_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        response = self.client.delete(f'/api/elections/campuses/{self.campus.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_campus_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(f'/api/elections/campuses/{self.campus.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class FacultyViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superadmin_user = get_user_model().objects.create_superuser(
            username='admin', password='adminpassword'
        )
        self.campus = CampusFactory()
        self.faculty = FacultyFactory()
        self.regular_user = get_user_model().objects.create_user(
            username='user', password='userpassword', person=PersonFactory()
        )

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
        self.client.force_authenticate(user=self.regular_user)
        data = {'name': 'New Faculty', 'campus_id': self.campus.id}
        response = self.client.post('/api/elections/faculties/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_faculty_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        data = {'name': 'Updated Faculty', 'campus_id': self.campus.id}
        response = self.client.put(f'/api/elections/faculties/{self.faculty.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_faculty_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {'name': 'Updated Faculty', 'campus_id': self.campus.id}
        response = self.client.put(f'/api/elections/faculties/{self.faculty.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_faculty_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        response = self.client.delete(f'/api/elections/faculties/{self.faculty.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_faculty_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(f'/api/elections/faculties/{self.faculty.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PersonViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/elections/people/'
        self.superadmin_user = get_user_model().objects.create_superuser(
            username='admin', password='adminpassword'
        )
        self.faculty = FacultyFactory()
        self.regular_user = get_user_model().objects.create_user(
            username='user', password='userpassword', person=PersonFactory()
        )
        self.person = PersonFactory()

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
        self.client.force_authenticate(user=self.regular_user)
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
        self.client.force_authenticate(user=self.regular_user)

        data = {'name': 'Updated', 'last_name': 'Person', 'faculty_id': self.faculty.id}
        response = self.client.put(f'{self.url}{self.person.ci}/', data)

        self.assertEqual(response.status_code, 200)
        self.person.refresh_from_db()
        self.assertEqual(self.person.name, 'Updated')
        self.assertEqual(response['Content-Type'], 'application/json')

        # Verificar el contenido de la respuesta (opcional)
        self.assertEqual(response.json(), {'ci': self.person.ci, 'name': 'Updated', 'last_name': 'Person',
                                           'faculty_id': self.faculty.id})

    def test_delete_person_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        response = self.client.delete(f'{self.url}{self.person.ci}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_person_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(f'{self.url}{self.person.ci}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ElectionViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superadmin_user = get_user_model().objects.create_superuser(
            username='admin', password='adminpassword'
        )
        self.regular_user = get_user_model().objects.create_user(
            username='user', password='userpassword', person=PersonFactory()
        )
        self.institution = InstitutionFactory()
        self.election = ElectionFactory()

    def test_list_elections(self):
        Election.objects.create(type='institution', location_id=self.institution.id, council_size=5,
                                voting_date=timezone.now(), is_active=False)
        response = self.client.get('/api/elections/elections/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_election(self):
        election = Election.objects.create(type='institution', location_id=self.institution.id, council_size=5,
                                           voting_date=timezone.now(), is_active=False)
        response = self.client.get(f'/api/elections/elections/{election.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_election_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        data = {
            'type': 'institution',
            'location_id': self.institution.id,
            'council_size': 5,
            'voting_date': timezone.now() + timedelta(days=30),
            'is_active': False,
        }
        response = self.client.post('/api/elections/elections/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_election_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {
            'type': 'institution',
            'location_id': self.institution.id,
            'council_size': 5,
            'voting_date': timezone.now(),
            'is_active': False,
        }
        response = self.client.post('/api/elections/elections/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_election_as_superuser(self):
        election = ElectionFactory()
        self.client.force_authenticate(user=self.superadmin_user)
        data = {
            'council_size': 10,
            'is_active': True,
        }
        response = self.client.patch(f'/api/elections/elections/{election.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_election_as_regular_user(self):
        election = ElectionFactory()
        self.client.force_authenticate(user=self.regular_user)
        data = {'name': 'Updated Election'}
        response = self.client.put(f'/api/elections/elections/{election.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_election_as_superuser(self):
        election = ElectionFactory()
        self.client.force_authenticate(user=self.superadmin_user)
        response = self.client.delete(f'/api/elections/elections/{election.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_election_as_regular_user(self):
        election = ElectionFactory()
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(f'/api/elections/elections/{election.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CandidateViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superadmin_user = get_user_model().objects.create_superuser(
            username='admin', password='adminpassword'
        )
        self.institution = Institution.objects.create(name='Test Institution')
        self.campus = Campus.objects.create(name='Test Campus', institution_id=self.institution)
        self.faculty = Faculty.objects.create(name='Test Faculty', campus_id=self.campus)
        self.election = Election.objects.create(type='institution', location_id=self.institution.id, council_size=5,
                                                voting_date=timezone.now(), is_active=False)
        self.person = PersonFactory()
        self.candidate_managers_group, created = Group.objects.get_or_create(name='Candidate Managers')
        self.user = get_user_model().objects.create_user(
            username='user', password='adminpassword', person=self.person, election_id=self.election
        )
        self.user.groups.add(self.candidate_managers_group)
        self.person_data = {
            'ci': '12345678901',
            'name': 'John',
            'last_name': 'Doe',
            'faculty_id': self.faculty.id,
        }
        self.candidate_data = {
            'person': self.person_data,
            'election_id': self.election.id,
            'biography': 'Test Biography',
            'who_added': 'committee',
            'staff_votes': 0,
            'president_votes': 0,
            'position': 'Test Position',
            'name': self.person_data['name'],  # Incluye el nombre de la persona
            'last_name': self.person_data['last_name'],  # Incluye el apellido de la persona
            'faculty_id': self.faculty.id,
        }

    def test_create_candidate_as_superuser(self):
        # Autenticar como superusuario
        self.client.force_authenticate(user=self.superadmin_user)
        url = reverse('candidate-list')
        response = self.client.post(url, self.candidate_data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Candidate.objects.count(), 1)

    def test_create_candidate_as_regular_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('candidate-list')
        response = self.client.post(url, self.candidate_data, format='json')
        print(response.content)
        # Verificar que el acceso sea denegado para usuarios regulares
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Candidate.objects.count(), 1)

    def test_create_candidate_as_regular_user_other_election(self):
        user = CustomUserFactory()
        user.groups.add(self.candidate_managers_group)
        self.client.force_authenticate(user=user)
        url = reverse('candidate-list')
        response = self.client.post(url, self.candidate_data, format='json')
        print(response.content)
        # Verificar que el acceso sea denegado para usuarios regulares
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Candidate.objects.count(), 0)

    def test_update_candidate_as_superuser(self):
        # Crear un candidato para actualizar
        candidate = CandidateFactory()

        # Autenticar como superusuario
        self.client.force_authenticate(user=self.superadmin_user)

        # Datos de ejemplo para la actualización del candidato
        updated_data = {
            'biography': 'Pene',
            'staff_votes': 10,
        }

        url = reverse('candidate-detail', args=[candidate.person.ci])
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        candidate.refresh_from_db()
        # Verificar que los datos del candidato se hayan actualizado correctamente
        self.assertEqual(candidate.biography, updated_data["biography"])
        self.assertEqual(candidate.staff_votes, updated_data["staff_votes"])

    def test_update_candidate_as_regular_user(self):
        candidate = CandidateFactory()
        candidate.election_id = self.user.election_id
        candidate.save()
        # Autenticar como superusuario
        self.client.force_authenticate(user=self.user)

        # Datos de ejemplo para la actualización del candidato
        updated_data = {
            'biography': 'Pene',
            'staff_votes': 10,
        }

        url = reverse('candidate-detail', args=[candidate.person.ci])
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        candidate.refresh_from_db()
        # Verificar que los datos del candidato se hayan actualizado correctamente
        self.assertEqual(candidate.biography, updated_data["biography"])
        self.assertEqual(candidate.staff_votes, updated_data["staff_votes"])

    def test_update_candidate_as_regular_user_other_election(self):
        candidate = CandidateFactory()
        self.client.force_authenticate(user=self.user)
        updated_data = {
            'biography': 'Pene',
            'staff_votes': 10,
        }
        url = reverse('candidate-detail', args=[candidate.person.ci])
        response = self.client.patch(url, updated_data, format='json')

        # Verificar que el acceso sea denegado para usuarios regulares
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_candidate_as_superuser(self):
        # Crear un candidato para eliminar
        candidate_data = CandidateFactory()

        # Autenticar como superusuario
        self.client.force_authenticate(user=self.superadmin_user)

        url = reverse('candidate-detail', args=[candidate_data.person.ci])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Candidate.objects.count(), 0)

    def test_delete_candidate_as_regular_user(self):
        # Crear un candidato para eliminar
        candidate_data = CandidateFactory()
        candidate_data.election_id = self.election
        candidate_data.save()

        self.client.force_authenticate(user=self.user)

        url = reverse('candidate-detail', args=[candidate_data.person.ci])
        response = self.client.delete(url)
        print(response.content)
        # Verificar que el acceso sea denegado para usuarios regulares
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Candidate.objects.count(), 0)

    def test_delete_candidate_as_regular_user_other_election(self):
        candidate = CandidateFactory()
        self.client.force_authenticate(user=self.user)
        url = reverse('candidate-detail', args=[candidate.person.ci])
        response = self.client.delete(url)

        # Verificar que el acceso sea denegado para usuarios regulares
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ElectorRegistryViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superadmin_user = get_user_model().objects.create_superuser(
            username='admin', password='adminpassword'
        )
        self.regular_user = get_user_model().objects.create_user(
            username='user', password='userpassword', person=PersonFactory()
        )
        self.institution = InstitutionFactory()
        self.election = ElectionFactory()
        self.person = PersonFactory()

    def test_list_elector_registry(self):
        # Crea algunos registros de ElectorRegistry para probar la lista
        ElectorRegistryFactory.create_batch(3)

        url = reverse('electorregistry-list')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4

    def test_create_elector_registry(self):
        # Crea instancias necesarias (puedes usar factories para esto)
        person = PersonFactory()
        election = ElectionFactory()
        candidate_0 = CandidateFactory()
        candidate_1 = CandidateFactory()
        candidate_2 = CandidateFactory()

        data = {
            'elector': {
                'ci': person.ci,
                'election_id': election.id
            },
            'candidates': {
                candidate_0.person.ci: {
                    'staff_votes': True,
                    'president_votes': False
                },
                candidate_1.person.ci: {
                    'staff_votes': True,
                    'president_votes': True
                },
                candidate_2.person.ci: {
                    'staff_votes': True,
                    'president_votes': False
                }
            }
        }

        url = reverse('electorregistry-list')
        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

        # Verifica que el registro se haya creado correctamente
        elector_registry = ElectorRegistry.objects.first()
        assert elector_registry.ci == person
        assert elector_registry.election_id == election
        candidate_0.refresh_from_db()
        candidate_1.refresh_from_db()
        candidate_2.refresh_from_db()
        assert candidate_0.staff_votes == 1
        assert candidate_1.staff_votes == 1
        assert candidate_1.president_votes == 1
        assert candidate_2.staff_votes == 1

    def test_retrieve_elector_registry(self):
        elector_registry = ElectorRegistry.objects.create(ci=self.person, election_id=self.election)

        url = reverse('electorregistry-detail', args=[elector_registry.id])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == ElectorRegistrySerializer(elector_registry).data


class CandidateLogViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superadmin_user = get_user_model().objects.create_superuser(
            username='admin', password='adminpassword'
        )
        self.person = PersonFactory()
        self.election = ElectionFactory()
        self.candidate_log = CandidateLog.objects.create(person=self.person, election_id=self.election, biography='Test Biography', who_added='committee', staff_votes=0, president_votes=0, position='Test Position')

    def test_list_candidate_logs(self):
        self.client.force_authenticate(user=self.superadmin_user)
        response = self.client.get('/api/elections/candidate-log/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_candidate_log(self):
        self.client.force_authenticate(user=self.superadmin_user)
        response = self.client.get(f'/api/elections/candidate-log/{self.candidate_log.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_candidate_log_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        data = {'person': self.person.ci, 'election_id': self.election.id, 'biography': 'New Biography', 'who_added': 'elector', 'staff_votes': 10, 'president_votes': 10, 'position': 'New Position'}
        response = self.client.post('/api/elections/candidate-log/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_candidate_log_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        data = {
            'biography': 'Updated Biography',
            'who_added': 'committee',
            'staff_votes': 20,
            'president_votes': 20,
            'position': 'Updated Position'
        }
        headers = {'content-type': 'application/json'}
        response = self.client.patch(f'/api/elections/candidate-log/{self.candidate_log.id}/', data=data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_candidate_log_as_superuser(self):
        self.client.force_authenticate(user=self.superadmin_user)
        response = self.client.delete(f'/api/elections/candidate-log/{self.candidate_log.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)