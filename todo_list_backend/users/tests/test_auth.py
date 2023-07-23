import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class TestUserAuthentication:
    """Testing user authentication"""

    @pytest.mark.django_db
    def test_registration(self, unauthenticated_api_client):
        """Tests successful user registration with valid details"""
        register_url = reverse("rest_register")
        user_data = {"email": "user@example.com", "password1": "test_password", "password2": "test_password"}
        response = unauthenticated_api_client.post(register_url, user_data)
        # Test that the response status code is 201 (created)
        assert response.status_code == 201
        # Test that the user received token
        response_data = response.json()
        assert "access" in response_data
        assert "refresh" in response_data

    @pytest.mark.django_db
    def test_user_already_registered(self, unauthenticated_api_client):
        """Tests unsuccessful registration with already registered email"""
        register_url = reverse("rest_register")
        user_data_for_creating_user = {"email": "user@example.com", "password": "test_password", "name": "Test User"}
        user_data_data_for_registering = {
            "email": "user@example.com",
            "password1": "test_password",
            "password2": "test_password",
        }
        create_user(**user_data_for_creating_user)

        response = unauthenticated_api_client.post(register_url, user_data_data_for_registering)

        assert response.status_code == 400

    @pytest.mark.django_db
    def test_registration_with_invalid_details(self, unauthenticated_api_client):
        """Tests unsucessful registration with invalid details"""
        register_url = reverse("rest_register")
        user_data = {"email": "user@example.com", "password1": "te", "password2": "te"}

        response = unauthenticated_api_client.post(register_url, user_data)

        assert response.status_code == 400
