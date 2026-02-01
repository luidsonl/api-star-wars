import pytest
import requests_mock
from unittest.mock import MagicMock, patch
from app.swapi_client import SWAPIClient

@pytest.fixture
def swapi_client():
    # Patch the cache repo to avoid firestore calls during these tests
    with patch('app.swapi_client.SWAPICacheRepository') as mock_repo:
        client = SWAPIClient()
        client.cache_repo = mock_repo.return_value
        yield client, client.cache_repo

def test_get_entity_success(swapi_client):
    client, mock_cache = swapi_client
    mock_cache.get_cached_response.return_value = None # Cache miss
    
    with requests_mock.Mocker() as m:
        url = "https://swapi.dev/api/people/1/"
        m.get(url, json={"name": "Luke Skywalker"})
        data = client.get_entity("people", "1")
        
        assert data["name"] == "Luke Skywalker"
        mock_cache.cache_response.assert_called_once_with(url, {"name": "Luke Skywalker"})

def test_get_entity_cache_hit(swapi_client):
    client, mock_cache = swapi_client
    mock_cache.get_cached_response.return_value = {"name": "C-3PO"}
    
    data = client.get_entity("people", "2")
    assert data["name"] == "C-3PO"
    # Should not make a request (requests_mock will fail if it does since we didn't mock any request)
    mock_cache.cache_response.assert_not_called()

def test_list_entities_no_params(swapi_client):
    client, mock_cache = swapi_client
    mock_cache.get_cached_response.return_value = None
    
    with requests_mock.Mocker() as m:
        url = "https://swapi.dev/api/planets/?page=1"
        expected_json = {"count": 1, "results": [{"name": "Tatooine"}]}
        m.get(url, json=expected_json)
        
        data = client.list_entities("planets")
        assert data == expected_json
        mock_cache.cache_response.assert_called_once_with(url, expected_json)

def test_list_entities_with_search(swapi_client):
    client, mock_cache = swapi_client
    mock_cache.get_cached_response.return_value = None
    
    with requests_mock.Mocker() as m:
        url = "https://swapi.dev/api/people/?page=1&search=r2"
        expected_json = {"count": 1, "results": [{"name": "R2-D2"}]}
        m.get(url, json=expected_json)
        
        data = client.list_entities("people", page=1, search="r2")
        assert data == expected_json
        mock_cache.cache_response.assert_called_once_with(url, expected_json)

def test_get_by_url(swapi_client):
    client, mock_cache = swapi_client
    mock_cache.get_cached_response.return_value = None
    
    with requests_mock.Mocker() as m:
        url = "https://swapi.dev/api/vehicles/4/"
        expected_json = {"name": "Sand Crawler"}
        m.get(url, json=expected_json)
        
        data = client.get_by_url(url)
        assert data == expected_json
        mock_cache.cache_response.assert_called_once_with(url, expected_json)
