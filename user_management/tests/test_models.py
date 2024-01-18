import json
import unittest

from django.urls import reverse
from django.contrib.auth import get_user_model

from django.test import TestCase
from django.http import JsonResponse
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone

from elections.tests.factory.models_factory import PersonFactory, ElectionFactory
from user_management.models import CustomUser, CustomUserLog


class UserManagerTests(TestCase):
    def test_create_user(self):
        """
        Test creating a regular user.
        """
        user = get_user_model().objects.create_user(username='testuser', password='testpassword',
                                                    person=PersonFactory())
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)

        self.assertIsNotNone(get_user_model().objects.get(username='testuser'))

        authenticated = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(authenticated)

    def test_create_superuser(self):
        """
        Test creating a superuser.
        """
        admin_user = get_user_model().objects.create_superuser(username='admin', password='adminpassword')
        self.assertEqual(admin_user.username, 'admin')
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        self.assertIsNotNone(get_user_model().objects.get(username='admin'))


class CustomUserTests(TestCase):
    def setUp(self):
        self.person = PersonFactory()
        self.election = ElectionFactory()

    def test_create_user_with_person(self):
        """
        Test creating a user with associated person.
        """
        user = CustomUser.objects.create_user(username='testuser', password='testpassword', person=self.person)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.person.ci, self.person.ci)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser_with_person_and_election(self):
        """
        Test creating a superuser with associated person and election.
        """
        admin_user = get_user_model().objects.create_superuser(username='admin', password='adminpassword')
        self.assertEqual(admin_user.username, 'admin')
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        self.assertIsNone(admin_user.person)
        self.assertIsNone(admin_user.election_id)

User = get_user_model()

class CustomUserLogViewSetTest(TestCase):
   def setUp(self):
       self.superadmin_user = User.objects.create_superuser(username='admin', password='adminpassword')
       self.client.login(username='admin', password='adminpassword')

   def test_create_custom_user_log(self):
       url = reverse('customuserlog-list')
       data = {
           'person': PersonFactory(),
           'username': 'testuser',
           'date_joined': timezone.now(),
           'is_staff': False,
           'is_superuser': False,
           'election_id': ElectionFactory(),
       }
       response = self.client.post(url, data, format='json')
       self.assertEqual(response.status_code, status.HTTP_201_CREATED)

   def test_read_custom_user_log(self):
       custom_user_log = CustomUserLog.objects.create(person=PersonFactory(), username='testuser', date_joined=timezone.now(), is_staff=False, is_superuser=False, election_id=ElectionFactory())
       url = reverse('customuserlog-detail', kwargs={'pk': custom_user_log.id})
       response = self.client.get(url)
       self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_update_custom_user_log(self):
       custom_user_log = CustomUserLog.objects.create(person=PersonFactory(), username='testuser', date_joined=timezone.now(), is_staff=False, is_superuser=False, election_id=ElectionFactory())
       url = reverse('customuserlog-detail', kwargs={'pk': custom_user_log.id})
       data = {
           'username': 'updateduser',
           'is_staff': True,
           'is_superuser': True,
       }
       response = self.client.patch(url, data, format='json')
       self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_delete_custom_user_log(self):
       custom_user_log = CustomUserLog.objects.create(person=PersonFactory(), username='testuser', date_joined=timezone.now(), is_staff=False, is_superuser=False, election_id=ElectionFactory())
       url = reverse('customuserlog-detail', kwargs={'pk': custom_user_log.id})
       response = self.client.delete(url)
       self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)