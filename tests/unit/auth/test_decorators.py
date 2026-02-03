import pytest
from unittest.mock import MagicMock, patch
from app.auth.service import AuthService

def test_token_required_user_not_exists(client, mock_db):
    """
    Test that a valid JWT token with a non-existent user_id is rejected.
    """
    user_id = "deleted-user-id"
    token = AuthService.generate_token(user_id)
    
    # Mock user_service.get_user_by_id to return None
    with patch('app.auth.decorators.user_service.get_user_by_id', return_value=None):
        response = client.get('/users/me', headers={
            'Authorization': f'Bearer {token}'
        })
        
        assert response.status_code == 401
        assert response.json['message'] == 'User not found or account disabled!'

def test_token_required_user_exists(client, mock_db):
    """
    Test that a valid JWT token with an existent user_id is accepted.
    """
    user_id = "existent-user-id"
    token = AuthService.generate_token(user_id)
    
    # Mock user exists
    mock_user = MagicMock()
    mock_user.id = user_id
    mock_user.email = "test@example.com"
    mock_user.name = "Test User"
    
    with patch('app.auth.decorators.user_service.get_user_by_id', return_value=mock_user):
        # We also need to patch it in the controller if it's used there
        with patch('app.user.controller.user_service.get_user_by_id', return_value=mock_user):
            response = client.get('/users/me', headers={
                'Authorization': f'Bearer {token}'
            })
            
            assert response.status_code == 200
            assert response.json['id'] == user_id
