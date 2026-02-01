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

def test_get_all_entities(swapi_client):
    client, mock_cache = swapi_client
    mock_cache.get_cached_response.return_value = None
    
    with requests_mock.Mocker() as m:
        url1 = "https://swapi.dev/api/people/"
        url2 = "https://swapi.dev/api/people/?page=2"
        
        m.get(url1, json={
            "next": url2,
            "results": [{"name": "Luke"}]
        })
        m.get(url2, json={
            "next": None,
            "results": [{"name": "Vader"}]
        })
        
        results = client.get_all_entities("people")
        assert len(results) == 2
        assert results[0]["name"] == "Luke"
        assert results[1]["name"] == "Vader"

def test_list_entities_with_sorting_numeric(swapi_client):
    client, mock_cache = swapi_client
    mock_cache.get_cached_response.return_value = None
    
    with requests_mock.Mocker() as m:
        url = "https://swapi.dev/api/people/"
        # Mocking get_all_entities indirectly by mocking the request
        m.get(url, json={
            "next": None,
            "results": [
                {"name": "Luke", "height": "172"},
                {"name": "Yoda", "height": "66"},
                {"name": "Chewie", "height": "228"}
            ]
        })
        
        # Sort by height ascending
        data = client.list_entities("people", sort_by="height")
        
        assert data["results"][0]["name"] == "Yoda"   # 66
        assert data["results"][1]["name"] == "Luke"   # 172
        assert data["results"][2]["name"] == "Chewie" # 228

def test_list_entities_with_sorting_unknown_numeric(swapi_client):
    client, mock_cache = swapi_client
    mock_cache.get_cached_response.return_value = None
    
    with requests_mock.Mocker() as m:
        url = "https://swapi.dev/api/people/"
        m.get(url, json={
            "next": None,
            "results": [
                {"name": "Luke", "height": "172"},
                {"name": "Artoo", "height": "96"},
                {"name": "Unknown", "height": "unknown"}
            ]
        })
        
        # Sort by height ascending. 'unknown' should be at the beginning (float('-inf'))
        data = client.list_entities("people", sort_by="height")
        
        assert data["results"][0]["name"] == "Unknown"
        assert data["results"][1]["name"] == "Artoo"
        assert data["results"][2]["name"] == "Luke"

def test_substitute_urls(swapi_client):
    client, mock_cache = swapi_client
    mock_cache.get_cached_response.return_value = {
        "count": 1,
        "next": "https://swapi.dev/api/people/?page=2",
        "previous": None,
        "results": [
            {
                "name": "Luke Skywalker",
                "homeworld": "https://swapi.dev/api/planets/1/",
                "films": ["https://swapi.dev/api/films/1/"]
            }
        ]
    }
    
    # Mock Flask request context
    from flask import Flask
    app = Flask(__name__)
    with app.test_request_context(base_url='http://myhosting.com/api/'):
        data = client.get_by_url("https://swapi.dev/api/people/1/")
        
        assert data["next"] == "http://myhosting.com/api/people/?page=2"
        assert data["results"][0]["homeworld"] == "http://myhosting.com/api/planets/1/"
        assert data["results"][0]["films"][0] == "http://myhosting.com/api/films/1/"

def test_substitute_urls_no_context(swapi_client):
    client, mock_cache = swapi_client
    mock_cache.get_cached_response.return_value = {
        "homeworld": "https://swapi.dev/api/planets/1/"
    }
    
    # No request context
    data = client.get_by_url("https://swapi.dev/api/people/1/")
    # Should be relative
    assert data["homeworld"] == "planets/1/"

def test_list_entities_sorting_pagination(swapi_client):
    client, mock_cache = swapi_client
    mock_cache.get_cached_response.return_value = None
    
    with requests_mock.Mocker() as m:
        url = "https://swapi.dev/api/people/"
        m.get(url, json={
            "next": None,
            "results": [{"name": f"Person {i}", "height": str(i)} for i in range(1, 16)]
        })
        
        from flask import Flask
        app = Flask(__name__)
        with app.test_request_context(base_url='http://myhosting.com/api/'):
            # Fetch page 1 (items 1-10) sorted by height
            data = client.list_entities("people", page=1, sort_by="height")
            
            assert data["count"] == 15
            assert len(data["results"]) == 10
            assert data["next"] == "http://myhosting.com/api/people/?page=2&sort_by=height"
            assert data["previous"] is None
            
            # Fetch page 2 (items 11-15) sorted by height
            data = client.list_entities("people", page=2, sort_by="height")
            assert data["next"] is None
            assert data["previous"] == "http://myhosting.com/api/people/?page=1&sort_by=height"
