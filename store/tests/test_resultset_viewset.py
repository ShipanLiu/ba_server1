# store/tests/test_resultset_viewset.py
import pytest
from rest_framework import status
from model_bakery import baker
from django.conf import settings
from core.models import User
from store.models import ResultSet, AiModel, Project, Customer, Image


@pytest.mark.django_db
class TestResultSetViewSet:

    # list / retrieve

    def test_list_result_sets_authenticated(self, api_client, project, ai_model, regular_user):
        api_client.force_authenticate(user=regular_user)
        for _ in range(3):
            image = baker.make(Image, project=project)
            baker.make(ResultSet, project=project, ai_model=ai_model, image=image)

        response = api_client.get(f"/store/projects/{project.id}/results/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_retrieve_result_set_authenticated(self, api_client, regular_user, result_set):
        api_client.force_authenticate(user=regular_user)
        # retrieve according to image_id, but not result_set_id
        response = api_client.get(f"/store/projects/{result_set.project.id}/results/{result_set.image.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == result_set.id


    # does not support creating resultsets via api.


