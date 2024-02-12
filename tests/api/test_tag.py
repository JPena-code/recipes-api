import pytest
from pytest import FixtureRequest

from fastapi import status
from fastapi.testclient import TestClient


class TestAPITag:

    model = {
        'name': 'TestTag'
    }
    resource_type = 'Tag'

    def test_tags(self, client: TestClient):
        response = client.get(
            '/api/1.0.0/tags',
            timeout=500
        )
        content = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert content['resource_type'] == TestAPITag.resource_type

    def test_create_tag(self, client: TestClient, login: dict[str, str]):
        headers = {
            'Authorization': f'Bearer {login["data"]["access_token"]}'
        }
        response = client.post(
            '/api/1.0.0/tags',
            headers=headers,
            json=TestAPITag.model,
            timeout=500
        )
        content = response.json()
        assert response.status_code == status.HTTP_201_CREATED
        assert content['resource_type'] == TestAPITag.resource_type
        assert content['data']['name'] == TestAPITag.model['name']
        TestAPITag.model['id'] = content['data']['id']

    def test_tag(self, client: TestClient):
        response = client.get(
            f'/api/1.0.0/tags/{TestAPITag.model["id"]}',
            timeout=500
        )
        content = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert content['resource_type'] == TestAPITag.resource_type
        assert content['data']['name'] == TestAPITag.model['name']
        assert content['data']['id'] == TestAPITag.model['id']

    @pytest.mark.parametrize(
            'logged',
            [
                'login',
                None
            ])
    def test_delete_tag(self, logged: str | None, client: TestClient, request: FixtureRequest):
        headers = {
            'Accept': 'application/json',
        }
        if logged:
            login = request.getfixturevalue(logged)
            headers.update({
                'Authorization': f'Bearer {login["data"]["access_token"]}'
            })
        response = client.delete(
            f'/api/1.0.0/tags/{TestAPITag.model["id"]}',
            headers=headers,
            timeout=500
        )
        content = response.json()
        if logged:
            assert response.status_code == status.HTTP_200_OK
            assert content['resource_type'] == TestAPITag.resource_type
        else:
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
            assert response.headers['WWW-Authenticate'] == 'Bearer'
            assert content['detail']['resource_type'] == 'Unauthenticated error'
