import pytest
from unittest.mock import MagicMock, patch

def test_get_people(client):
    with patch('app.people.controller.people_service') as mock_service:
        mock_service.list_people.return_value = {"results": [{"name": "Luke Skywalker"}]}
        
        response = client.get('/people/?page=1&search=Luke&sort_by=height')
        
        mock_service.list_people.assert_called_once_with(page=1, search="Luke", sort_by="height")
        assert response.status_code == 200
        assert response.json['results'][0]['name'] == "Luke Skywalker"

def test_get_person(client):
    with patch('app.people.controller.people_service') as mock_service:
        mock_service.get_person.return_value = {"name": "Luke Skywalker"}
        
        response = client.get('/people/1')
        
        mock_service.get_person.assert_called_once_with("1")
        assert response.status_code == 200
        assert response.json['name'] == "Luke Skywalker"

def test_get_person_not_found(client):
    with patch('app.people.controller.people_service') as mock_service:
        mock_service.get_person.return_value = None
        
        response = client.get('/people/999')
        
        assert response.status_code == 404
        assert response.json['error'] == "Person not found"
