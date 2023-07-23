import pytest
from django.urls import reverse


class TestUserAuthentication:
    """Testing user authentication"""

    @pytest.mark.django_db
    def test_registration(self, unauthenticated_api_client):
        register_url = reverse("rest_register")
        user_data = {"email": "user@example.com", "password1": "test_password", "password2": "test_password"}
        response = unauthenticated_api_client.post(register_url, user_data)
        # Test that the response status code is 201 (created)
        assert response.status_code == 201
        # Test that the user received token
        response_data = response.json()
        assert "access" in response_data
        assert "refresh" in response_data

    # @pytest.mark.django_db
