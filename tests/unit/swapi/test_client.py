import pytest
import requests_mock
from app.swapi_client import SWAPIClient

@pytest.fixture
def swapi_client():
    return SWAPIClient()

def test_get_entity_success(swapi_client):
    with requests_mock.Mocker() as m:
        m.get("https://swapi.dev/api/people/1/", json={"name": "Luke Skywalker"})
        data = swapi_client.get_entity("people", "1")
        assert data["name"] == "Luke Skywalker"

def test_get_entity_not_found(swapi_client):
    with requests_mock.Mocker() as m:
        m.get("https://swapi.dev/api/people/999/", status_code=404)
        data = swapi_client.get_entity("people", "999")
        assert data is None

def test_get_entity_server_error(swapi_client):
    with requests_mock.Mocker() as m:
        m.get("https://swapi.dev/api/people/1/", status_code=500)
        data = swapi_client.get_entity("people", "1")
        assert data is None
