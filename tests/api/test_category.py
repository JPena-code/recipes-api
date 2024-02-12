import pytest
from pytest import FixtureRequest

from fastapi import status
from fastapi.testclient import TestClient


class TestAPICategory:

    model = {
        'name': 'TestCategory'
    }
    resource_type = 'Category'

    def test_categories(self, client: TestClient):
        response = client.get(
            '/api/1.0.0/categories',
            timeout=500
        )
        content = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert content['resource_type'] == TestAPICategory.resource_type

    def test_create_category(self, client: TestClient, login: dict[str, str]):
        headers = {
            'Authorization': f'Bearer {login["data"]["access_token"]}'
        }
        response = client.post(
            '/api/1.0.0/categories',
            headers=headers,
            json=TestAPICategory.model,
            timeout=500
        )
        content = response.json()
        assert response.status_code == status.HTTP_201_CREATED
        assert content['resource_type'] == TestAPICategory.resource_type
        assert content['data']['name'] == TestAPICategory.model['name']
        TestAPICategory.model['id'] = content['data']['id']

    def test_category(self, client: TestClient):
        response = client.get(
            f'/api/1.0.0/categories/{TestAPICategory.model["id"]}',
            timeout=500
        )
        content = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert content['resource_type'] == TestAPICategory.resource_type
        assert content['data']['name'] == TestAPICategory.model['name']
        assert content['data']['id'] == TestAPICategory.model['id']

    @pytest.mark.parametrize(
            'logged',
            [
                'login',
                None
            ])
    def test_delete_category(self, logged: str | None, client: TestClient, request: FixtureRequest):
        headers = {
            'Accept': 'application/json',
        }
        if logged:
            login = request.getfixturevalue(logged)
            headers.update({
                'Authorization': f'Bearer {login["data"]["access_token"]}'
            })
        response = client.delete(
            f'/api/1.0.0/categories/{TestAPICategory.model["id"]}',
            headers=headers,
            timeout=500
        )
        content = response.json()
        if logged:
            assert response.status_code == status.HTTP_200_OK
            assert content['resource_type'] == TestAPICategory.resource_type
        else:
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
            assert response.headers['WWW-Authenticate'] == 'Bearer'
            assert content['detail']['resource_type'] == 'Unauthenticated error'
