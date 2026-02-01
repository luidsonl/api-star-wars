import pytest
from unittest.mock import MagicMock, patch
import requests_mock
from app.people.service import PeopleService

@pytest.fixture
def people_service():
    with patch('app.people.service.SWAPIClient') as mock_client:
        service = PeopleService()
        service.swapi_client = mock_client.return_value
        yield service, mock_client.return_value

def test_list_people(people_service):
    service, mock_client = people_service
    mock_client.list_entities.return_value = {"results": [{"name": "Luke Skywalker"}]}
    
    result = service.list_people(page=1, search="Luke", sort_by="height")
    
    mock_client.list_entities.assert_called_once_with('people', page=1, search="Luke", sort_by="height")
    assert result["results"][0]["name"] == "Luke Skywalker"

def test_get_person(people_service):
    service, mock_client = people_service
    mock_client.get_entity.return_value = {"name": "Darth Vader"}
    
    result = service.get_person("4")
    
    mock_client.get_entity.assert_called_once_with('people', "4")
    assert result["name"] == "Darth Vader"
