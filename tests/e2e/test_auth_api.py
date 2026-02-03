import pytest
from unittest.mock import MagicMock
from app.auth.service import AuthService

def test_register_success(client, mock_db):
    # Obtém a coleção mock que o UserService já possui
    mock_collection = mock_db.collection.return_value
    
    # Mock get_user_by_email para retornar None (usuário não existe)
    # UserService usa self.collection.where('email', '==', email).limit(1).stream()
    mock_query = mock_collection.where.return_value.limit.return_value
    mock_query.stream.return_value = []
    
    # Mock add para retornar (None, mock_doc)
    mock_doc = MagicMock()
    mock_doc.id = "test-user-id"
    mock_collection.add.return_value = (None, mock_doc)
    
    response = client.post('/auth/register', json={
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User"
    })
    
    assert response.status_code == 201
    assert response.json['id'] == "test-user-id"
    assert "token" in response.json
    assert response.json['user']['email'] == "test@example.com"
    assert response.json['user']['name'] == "Test User"

def test_login_success(client, mock_db):
    # Obtém a coleção mock que o UserService já possui
    mock_collection = mock_db.collection.return_value
    
    hashed_password = AuthService.hash_password("pass123")
    
    mock_user_doc = MagicMock()
    mock_user_doc.id = "test-user-id"
    mock_user_doc.to_dict.return_value = {
        "email": "test@example.com",
        "password_hash": hashed_password,
        "name": "Test User"
    }
    
    mock_query = mock_collection.where.return_value.limit.return_value
    mock_query.stream.return_value = [mock_user_doc]
    
    response = client.post('/auth/login', json={
        "email": "test@example.com",
        "password": "pass123"
    })
    
    assert response.status_code == 200
    assert "token" in response.json
    assert response.json['user']['email'] == "test@example.com"
    assert response.json['user']['name'] == "Test User"
