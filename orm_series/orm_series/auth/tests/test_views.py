# core/tests.py or core/tests/test_auth_views.py

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

# Get the custom User model if you have one, otherwise it's Django's default User
User = get_user_model()


class RegisterViewTest(APITestCase):
    """
    Test suite for the RegisterView.
    """

    def setUp(self):
        # Assuming the URL for RegisterView is named 'register' in your urls.py
        self.register_url = reverse('register')

    def test_user_registration_success(self):
        """
        Ensure a new user can be registered successfully with valid data.
        """
        data = {
            'username': 'newuser',
            'password': 'strongpassword123',
            'email': 'newuser@example.com'
        }
        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User created successfully')
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertEqual(User.objects.count(), 1)

    def test_user_registration_existing_username(self):
        """
        Ensure registration fails with a 400 Bad Request if the username already exists.
        """
        # Create a user first to simulate an existing username
        User.objects.create_user(username='existinguser', password='password123', email='existing@example.com')

        data = {
            'username': 'existinguser', # This username already exists
            'password': 'anotherpassword',
            'email': 'duplicate@example.com'
        }
        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Username already exists')
        self.assertEqual(User.objects.count(), 1)

    def test_user_registration_missing_username(self):
        """
        Ensure registration fails with a 400 Bad Request if the username is missing.
        """
        data = {
            'password': 'testpassword',
            'email': 'test@example.com'
        }
        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Username is required.')
        self.assertEqual(User.objects.count(), 0)

    def test_user_registration_missing_password(self):
        """
        Ensure registration fails with a 400 Bad Request if the password is missing.
        """
        data = {
            'username': 'testuser',
            'email': 'test@example.com'
        }
        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Password is required.')
        self.assertEqual(User.objects.count(), 0)

    def test_user_registration_empty_username_and_password(self):
        """
        Ensure registration fails with 400 Bad Request for empty username and password.
        """
        data = {
            'username': '',
            'password': '',
            'email': 'empty@example.com'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response.data['error'], 'Username is required.')
        self.assertEqual(User.objects.count(), 0)

