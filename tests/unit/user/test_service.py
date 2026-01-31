import pytest
from unittest.mock import MagicMock
from app.user.service import UserService
from app.user.model import User

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def service(mock_db):
    return UserService(database=mock_db)

def test_user_service_get_by_email_success(service, mock_db):
    mock_doc = MagicMock()
    mock_doc.id = "123"
    mock_doc.to_dict.return_value = {"email": "test@test.com", "name": "Test", "password_hash": "hash"}
    
    mock_db.collection.return_value.where.return_value.limit.return_value.stream.return_value = [mock_doc]
    
    user = service.get_user_by_email("test@test.com")
    assert user.id == "123"
    assert user.email == "test@test.com"

def test_user_service_get_by_email_none(service, mock_db):
    mock_db.collection.return_value.where.return_value.limit.return_value.stream.return_value = []
    user = service.get_user_by_email("none@test.com")
    assert user is None

def test_create_user_success(service, mock_db):
    user = User(id=None, email="new@test.com", name="New", password_hash="hash")
    
    # Mock search by email (none exists)
    mock_db.collection.return_value.where.return_value.limit.return_value.stream.return_value = []
    
    # Mock add
    mock_doc = MagicMock()
    mock_doc.id = "new123"
    mock_db.collection.return_value.add.return_value = (None, mock_doc)
    
    uid = service.create_user(user)
    assert uid == "new123"

def test_create_user_already_exists(service, mock_db):
    user = User(id=None, email="exists@test.com", name="E", password_hash="h")
    mock_db.collection.return_value.where.return_value.limit.return_value.stream.return_value = [MagicMock()]
    
    with pytest.raises(ValueError, match="already exists"):
        service.create_user(user)
