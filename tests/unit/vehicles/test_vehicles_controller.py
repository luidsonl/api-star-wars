from unittest.mock import patch

def test_get_vehicles(client):
    with patch('app.vehicles.controller.vehicles_service') as mock_service:
        mock_service.list_vehicles.return_value = {"results": [{"name": "Sand Crawler"}]}
        
        response = client.get('/vehicles/')
        
        assert response.status_code == 200
        assert response.json['results'][0]['name'] == "Sand Crawler"

def test_get_vehicle(client):
    with patch('app.vehicles.controller.vehicles_service') as mock_service:
        mock_service.get_vehicle.return_value = {"name": "Sand Crawler"}
        
        response = client.get('/vehicles/1')
        
        assert response.status_code == 200
        assert response.json['name'] == "Sand Crawler"

