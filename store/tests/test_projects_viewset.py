# store/tests/test_projects_viewset.py
import pytest
from rest_framework import status
from django.conf import settings
from store.models import Project, Image, AiModel
from model_bakery import baker

import tempfile
from PIL import Image as PILImage

@pytest.mark.django_db
class TestProjectsViewSet:

    # list

    def test_list_projects_authenticated(self, api_client, regular_user):
        api_client.force_authenticate(user=regular_user)
        baker.make(Project, _quantity=3, customer=regular_user.customer)
        response = api_client.get("/store/projects/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 3

    def test_retrieve_project_authenticated(self, api_client, regular_user, project):
        api_client.force_authenticate(user=regular_user)
        response = api_client.get(f"/store/projects/{project.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == project.name


    # create

    def test_create_project_unauthenticated(self, api_client, ai_model):
        project_data = {
            "name": "Test Project Unauth",
            "description": "Test Description Unauth",
            "ai_model_id": ai_model.id
        }
        response = api_client.post("/store/projects/", project_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_project_authenticated(self, api_client, regular_user, ai_model):
        api_client.force_authenticate(user=regular_user)
        project_data = {
            "name": "Test Project Auth",
            "description": "Test Description Auth",
            "ai_model_id": ai_model.id
        }
        response = api_client.post("/store/projects/", project_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == project_data['name']
        assert 'id' in response.data


    # update
    def test_update_project_authenticated(self, api_client, regular_user, project):
        api_client.force_authenticate(user=regular_user)
        updated_data = {"name": "Updated Project Name", "description": "Updated Description"}
        response = api_client.patch(f"/store/projects/{project.id}/", updated_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == updated_data['name']
        assert response.data['description'] == updated_data['description']



    # delete
    def test_delete_project_authenticated(self, api_client, regular_user, project):
        api_client.force_authenticate(user=regular_user)
        response = api_client.delete(f"/store/projects/{project.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Project.objects.filter(id=project.id).exists() is False


# Test for images Operation

    def test_upload_image_authenticated(self, api_client, regular_user, project):
        api_client.force_authenticate(user=regular_user)

        # Create a temporary image file
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as img:
            image = PILImage.new("RGB", (100, 100))
            image.save(img, format='JPEG')
            img.seek(0)  # Go back to the beginning of the file

            # Assuming the endpoint expects 'image_file' as the field name
            data = {'images': img}
            response = api_client.post(f"/store/projects/{project.id}/images/", data, format='multipart')

        assert response.status_code == status.HTTP_201_CREATED


    def test_view_image_authenticated(self, api_client, regular_user, project, image):
        api_client.force_authenticate(user=regular_user)
        response = api_client.get(f"/store/projects/{project.id}/images/{image.id}/")
        assert response.status_code == status.HTTP_200_OK

    def test_delete_image_authenticated(self, api_client, regular_user, project, image):
        api_client.force_authenticate(user=regular_user)
        response = api_client.delete(f"/store/projects/{project.id}/images/{image.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        # Verify the image has been deleted
        assert not Image.objects.filter(id=image.id).exists()