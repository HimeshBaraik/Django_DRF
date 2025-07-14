from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class AuthTests(APITestCase):

    def setUp(self):
        # Create a test user for login/logout/dashboard/profile tests
        self.test_user = User.objects.create_user(username="testuser", password="testpass123", email="test@example.com")

    def test_register_success(self):
        url = reverse('register')
        data = {
            "username": "newuser",
            "password": "newpass123",
            "email": "newuser@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "User created successfully")

    def test_register_missing_username(self):
        url = reverse('register')
        data = {
            "password": "newpass123",
            "email": "newuser@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Username is required", response.data["error"])

    def test_register_existing_username(self):
        url = reverse('register')
        data = {
            "username": "testuser",  # Already exists
            "password": "pass123",
            "email": "test@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Username already exists", response.data["error"])

    def test_login_success(self):
        url = reverse('jwt-login')
        data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        url = reverse('jwt-login')
        data = {
            "username": "testuser",
            "password": "wrongpass"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Invalid credentials", response.data["error"])

    def test_login_missing_fields(self):
        url = reverse('jwt-login')
        data = {
            "username": "testuser"
            # Missing password
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Username and password are required", response.data["error"])

    def test_dashboard_authenticated(self):
        url = reverse('dashboard')
        # Obtain token
        login_url = reverse('jwt-login')
        login_resp = self.client.post(login_url, {"username":"testuser", "password":"testpass123"}, format='json')
        token = login_resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Welcome testuser", response.data["message"])

    def test_dashboard_unauthenticated(self):
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_authenticated(self):
        url = reverse('profile')
        login_url = reverse('jwt-login')
        login_resp = self.client.post(login_url, {"username":"testuser", "password":"testpass123"}, format='json')
        token = login_resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")
        self.assertEqual(response.data["email"], "test@example.com")
        self.assertFalse(response.data["is_staff"])

    def test_logout_missing_refresh_token(self):
        login_url = reverse('jwt-login')
        login_resp = self.client.post(login_url, {"username":"testuser", "password":"testpass123"}, format='json')
        access_token = login_resp.data['access']

        url = reverse('logout')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
