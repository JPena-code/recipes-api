from pathlib import Path

import pytest
from dotenv import dotenv_values
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope='session', name='client')
def app_client():
    """Create the test httpx client to interact with the API"""
    client = TestClient(
        app,
        backend='asyncio',
        raise_server_exceptions=True,
        backend_options={'use_uvloop': True},
        headers={
            'Accept': 'application/json',
        },
    )
    yield client
    client.close()


@pytest.fixture(scope='session')
def login(client: TestClient):
    """Perform the login in the API and return the response content"""
    env_file = Path(__file__).absolute().parent.joinpath('client/.env')
    envs = dotenv_values(env_file.absolute())
    response = client.post(
        '/api/login',
        json={
            'email': envs.get('EMAIL', 'Should be an email'),
            'password': envs.get('PASSWORD', 'Should be an email')
        },
        timeout=500
    )
    yield response.json()
