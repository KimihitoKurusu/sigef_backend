from django.contrib.auth import get_user_model
from django.test import TestCase


class UserManagerTests(TestCase):
    def test_create_user(self):
        """
        Test creating a regular user.
        """
        user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.assertEqual(user.username, 'testuser')
        self.assertFalse(user.is_staff)
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
        from elections.models import Person, Election

        self.person = Person.objects.create(ci='12345678901', name='John', last_name='Doe')
        self.election = Election.objects.create(type='institution', location_id=1, council_size=5,
                                                voting_date='2022-01-01', is_active=True)

    def test_create_user_with_person(self):
        """
        Test creating a user with associated person.
        """
        user = get_user_model().objects.create_user(username='testuser', password='testpassword', create_person=True,
                                                    person=self.person)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.person, self.person)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        self.assertEqual(user.person, self.person)

    def test_create_superuser_with_person_and_election(self):
        """
        Test creating a superuser with associated person and election.
        """
        admin_user = get_user_model().objects.create_superuser(username='admin', password='adminpassword',
                                                               create_person=True)
        self.assertEqual(admin_user.username, 'admin')
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        self.assertIsNone(admin_user.person)
        self.assertIsNone(admin_user.election_id)