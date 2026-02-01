import pytest
from unittest.mock import MagicMock, patch
from app.database.swapi_cache_repo import SWAPICacheRepository

@pytest.fixture
def cache_repo():
    with patch('app.database.swapi_cache_repo.db') as mock_db:
        repo = SWAPICacheRepository()
        yield repo, mock_db

def test_get_url_hash(cache_repo):
    repo, _ = cache_repo
    url = "https://swapi.dev/api/people/1/"
    expected_hash = "8acd802949f8bae79ecef9232ffaf9e6bda99802f40dc9d009c52da60a170f81"
    assert repo._get_url_hash(url) == expected_hash

def test_get_cached_response_hit(cache_repo):
    repo, mock_db = cache_repo
    url = "https://swapi.dev/api/people/1/"
    mock_data = {"name": "Luke Skywalker"}
    
    mock_doc = MagicMock()
    mock_doc.exists = True
    mock_doc.to_dict.return_value = {'data': mock_data}
    
    mock_db.collection().document().get.return_value = mock_doc
    
    result = repo.get_cached_response(url)
    assert result == mock_data

def test_get_cached_response_miss(cache_repo):
    repo, mock_db = cache_repo
    url = "https://swapi.dev/api/people/1/"
    
    mock_doc = MagicMock()
    mock_doc.exists = False
    
    mock_db.collection().document().get.return_value = mock_doc
    
    result = repo.get_cached_response(url)
    assert result is None

def test_cache_response(cache_repo):
    repo, mock_db = cache_repo
    url = "https://swapi.dev/api/people/1/"
    mock_data = {"name": "Luke Skywalker"}
    
    repo.cache_response(url, mock_data)
    
    mock_db.collection().document().set.assert_called_once()
    args, _ = mock_db.collection().document().set.call_args
    assert args[0]['url'] == url
    assert args[0]['data'] == mock_data
    assert 'created_at' in args[0]
