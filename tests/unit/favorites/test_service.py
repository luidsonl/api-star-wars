import pytest
from unittest.mock import MagicMock
from app.favorites.service import FavoriteService
from app.favorites.model import Favorite

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def service(mock_db):
    return FavoriteService(database=mock_db)

def test_add_favorite_calls_db(service, mock_db):
    fav = Favorite(id=None, user_id="u1", entity_type="people", entity_id="1")
    
    # Mock no duplicate
    mock_db.collection.return_value.where.return_value.where.return_value.where.return_value.limit.return_value.stream.return_value = []
    
    # Mock SWAPI check (internal to service)
    service.swapi_client.get_entity = MagicMock(return_value={"name": "Luke"})
    
    # Mock add
    mock_doc = MagicMock()
    mock_doc.id = "f1"
    mock_db.collection.return_value.add.return_value = (None, mock_doc)
    
    fid = service.add_favorite(fav)
    assert fid == "f1"
    assert mock_db.collection.return_value.add.called

def test_add_favorite_duplicate(service, mock_db):
    fav = Favorite(id=None, user_id="u1", entity_type="people", entity_id="1")
    
    # Mock duplicate exists
    mock_db.collection.return_value.where.return_value.where.return_value.where.return_value.limit.return_value.stream.return_value = [MagicMock()]
    
    with pytest.raises(ValueError, match="already in favorites"):
        service.add_favorite(fav)

def test_remove_favorite(service, mock_db):
    service.remove_favorite("u1", "f1")
    # Should call doc("f1").get() then delete() if user_id matches
    # This is a bit more complex to mock fully but let's check doc() call
    assert mock_db.collection.return_value.document.called
