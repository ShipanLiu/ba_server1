import pytest
from rest_framework import status

@pytest.mark.django_db
class TestUserAuthentication:
    def test_refresh_jwt_token(self, api_client, user_and_tokens):
        refresh_data = {"refresh": user_and_tokens['refresh_token']}
        response = api_client.post("/auth/jwt/refresh", refresh_data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
