import pytest
from unittest.mock import MagicMock
import requests_mock
from app.auth.service import AuthService

def test_add_favorite_success(client, mock_db):
    # Register and get token
    user_id = "test-user-id"
    token = AuthService.generate_token(user_id)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get the collection mock
    mock_collection = mock_db.collection.return_value
    
    # Mock check if already exists
    # FavoriteService uses: self.collection.where(...).where(...).where(...).limit(1).stream()
    mock_query = mock_collection.where.return_value.where.return_value.where.return_value.limit.return_value
    mock_query.stream.return_value = []
    
    # Mock SWAPI valid entity check
    with requests_mock.Mocker() as m:
        m.get("https://swapi.dev/api/people/1/", json={"name": "Luke Skywalker"})
        
        # Mock add
        mock_doc = MagicMock()
        mock_doc.id = "fav-id"
        mock_collection.add.return_value = (None, mock_doc)
        
        response = client.post('/favorites/', json={
            "entity_type": "people",
            "entity_id": "1"
        }, headers=headers)
        
        assert response.status_code == 201
        assert response.json['id'] == "fav-id"

def test_list_favorites_success(client, mock_db):
    user_id = "test-user-id"
    token = AuthService.generate_token(user_id)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get the collection mock
    mock_collection = mock_db.collection.return_value
    
    mock_fav_doc = MagicMock()
    mock_fav_doc.id = "fav-id"
    mock_fav_doc.to_dict.return_value = {
        "user_id": user_id,
        "entity_type": "people",
        "entity_id": "1"
    }
    
    mock_query = mock_collection.where.return_value
    mock_query.stream.return_value = [mock_fav_doc]
    
    # Mock SWAPI
    with requests_mock.Mocker() as m:
        m.get("https://swapi.dev/api/people/1/", json={"name": "Luke Skywalker"})
        
        response = client.get('/favorites/', headers=headers)
        
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['data']['name'] == "Luke Skywalker"
