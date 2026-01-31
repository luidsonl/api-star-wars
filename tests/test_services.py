import pytest
from unittest.mock import MagicMock
from app.user.service import UserService
from app.user.model import User

def test_user_service_get_by_email():
    mock_db = MagicMock()
    service = UserService(database=mock_db)
    
    mock_doc = MagicMock()
    mock_doc.id = "123"
    mock_doc.to_dict.return_value = {"email": "test@test.com", "name": "Test", "password_hash": "hash"}
    
    mock_db.collection.return_value.where.return_value.limit.return_value.stream.return_value = [mock_doc]
    
    user = service.get_user_by_email("test@test.com")
    assert user.id == "123"
    assert user.email == "test@test.com"
