# conftest.py
import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from model_bakery import baker

from store.models import AiModel, Project, ResultSet, Image
from django.conf import settings

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticate_user(api_client):
    def do_authenticate(is_admin=False):
        user = baker.make(settings.AUTH_USER_MODEL, is_staff=is_admin)
        api_client.force_authenticate(user=user)
        return user
    return do_authenticate

@pytest.fixture
def regular_user():
    # Creates a regular user (non-admin)
    return baker.make(settings.AUTH_USER_MODEL, is_staff=False)

@pytest.fixture
def admin_user():
    # Creates an admin user
    return baker.make(settings.AUTH_USER_MODEL, is_staff=True, is_superuser=True)


@pytest.fixture
def ai_model():
    return baker.make(AiModel)

@pytest.fixture
def project(ai_model, regular_user):
    # Ensure that project uses the customer associated with the unique regular user
    return baker.make(Project, ai_model=ai_model, customer=regular_user.customer)

@pytest.fixture
def image(project):
    return baker.make(Image, project=project)


@pytest.fixture
def result_set(project, ai_model):
    image = baker.make(Image, project=project)
    return baker.make(ResultSet, project=project, ai_model=ai_model, image=image)


@pytest.fixture
def user_and_tokens(api_client):
    # Create a user
    user_data = {
        "username": "user2",
        "password": "19980223",
        "email": "user2@email.com",
        "first_name": "UserTwo",
        "last_name": "Liu"
    }
    api_client.post("/auth/users/", user_data)

    # Obtain JWT tokens
    credentials = {"username": "user2", "password": "19980223"}
    response = api_client.post("/auth/jwt/create", credentials)
    return {
        "user": user_data,
        "access_token": response.data['access'],
        "refresh_token": response.data['refresh']
    }