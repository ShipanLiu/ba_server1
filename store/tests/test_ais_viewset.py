import pytest
from rest_framework import status
from model_bakery import baker
from django.conf import settings


@pytest.mark.django_db
class TestAIsViewSet:
    def test_create_ai_model_unauthorized(self, api_client):
        ai_model_data = {"name": "AI Model Unauth", "description": "Description Unauth"}
        response = api_client.post("/store/ais/", ai_model_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_ai_model_non_admin(self, api_client):
        user = baker.make(settings.AUTH_USER_MODEL, is_staff=False)
        api_client.force_authenticate(user=user)
        ai_model_data = {"name": "AI Model Non-Admin", "description": "Description Non-Admin"}
        response = api_client.post("/store/ais/", ai_model_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_ai_model_admin(self, api_client):
        admin_user = baker.make(settings.AUTH_USER_MODEL, is_staff=True)
        api_client.force_authenticate(user=admin_user)
        ai_model_data = {"name": "Test AI Model", "description": "Test Description"}
        response = api_client.post("/store/ais/", ai_model_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == "Test AI Model"
        assert 'id' in response.data

    def test_list_ai_models_unauthenticated(self, api_client, ai_model):
        response = api_client.get("/store/ais/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_ai_models_authenticated(self, api_client, ai_model, regular_user):
        api_client.force_authenticate(user=regular_user)
        response = api_client.get("/store/ais/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['name'] == ai_model.name

    def test_retrieve_ai_model_authenticated(self, api_client, ai_model, regular_user):
        api_client.force_authenticate(user=regular_user)
        response = api_client.get(f"/store/ais/{ai_model.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == ai_model.name


