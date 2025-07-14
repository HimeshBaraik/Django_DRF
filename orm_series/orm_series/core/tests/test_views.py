from django.test import TestCase
from django.urls import reverse # Used to get URLs by name
from rest_framework import status
from rest_framework.test import APITestCase # Use APITestCase for API views

# Assuming your HomeView is in core.views
# from core.views import HomeView # Not strictly necessary if using reverse()

class HomeViewAPITest(APITestCase):
    """
    Test suite for the HomeView API.
    """

    def setUp(self):
        self.url = reverse('core-home') # Changed to 'core-home' as per your urls.py

    def test_home_view_get_request(self):
        """
        Test that the HomeView returns the expected welcome message and URLs.
        """
        response = self.client.get(self.url) # self.client is correctly used here

        # 1. Assert that the status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2. Assert that the response data contains the expected message
        self.assertIn("message", response.data)
        self.assertEqual(
            response.data["message"],
            "Welcome to the core app homepage! Here are the available API endpoints:"
        )

        # 3. Assert that the 'available_urls' list matches the expected list
        expected_urls = [
            "/allrestaurants",
            "/allrestaurantsbytype",
            "/allsales",
            "/allratings",
            "/counttotalrestaurants",
            "/staff/<int:pk>/restaurants/",
            "/restaurant/<int:pk>/staff/",
            "restaurants/add/",
        ]
        self.assertIn("available_urls", response.data)
        self.assertEqual(response.data["available_urls"], expected_urls)

    def test_home_view_no_authentication_required(self):
        """
        Test that the HomeView can be accessed without authentication.
        (This is implicitly tested by test_home_view_get_request, but explicit is good)
        """
        # Ensure no user is authenticated
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)