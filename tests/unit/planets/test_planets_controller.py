from unittest.mock import patch

def test_get_planets(client):
    with patch('app.planets.controller.planets_service') as mock_service:
        mock_service.list_planets.return_value = {"results": [{"name": "Tatooine"}]}
        
        response = client.get('/planets/')
        
        assert response.status_code == 200
        assert response.json['results'][0]['name'] == "Tatooine"

def test_get_planet(client):
    with patch('app.planets.controller.planets_service') as mock_service:
        mock_service.get_planet.return_value = {"name": "Tatooine"}
        
        response = client.get('/planets/1')
        
        assert response.status_code == 200
        assert response.json['name'] == "Tatooine"
