from django.urls import reverse
import pytest
from rest_framework import status


@pytest.mark.django_db
def test_user_registeration(api_client, user_data):
    url = reverse("users:register")
    response = api_client.post(url, user_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["username"] == user_data["username"]
