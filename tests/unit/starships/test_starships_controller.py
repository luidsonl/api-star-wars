from unittest.mock import patch

def test_get_starships(client):
    with patch('app.starships.controller.starships_service') as mock_service:
        mock_service.list_starships.return_value = {"results": [{"name": "Death Star"}]}
        
        response = client.get('/starships/')
        
        assert response.status_code == 200
        assert response.json['results'][0]['name'] == "Death Star"

def test_get_starship(client):
    with patch('app.starships.controller.starships_service') as mock_service:
        mock_service.get_starship.return_value = {"name": "Death Star"}
        
        response = client.get('/starships/1')
        
        assert response.status_code == 200
        assert response.json['name'] == "Death Star"
