from unittest.mock import patch
from app.vehicles.service import VehiclesService

def test_list_vehicles():
    with patch('app.vehicles.service.SWAPIClient') as mock_client:
        service = VehiclesService()
        mock_client.return_value.list_entities.return_value = {"results": [{"name": "Sand Crawler"}]}
        
        result = service.list_vehicles()
        
        assert result["results"][0]["name"] == "Sand Crawler"

def test_get_vehicle():
    with patch('app.vehicles.service.SWAPIClient') as mock_client:
        service = VehiclesService()
        mock_client.return_value.get_entity.return_value = {"name": "TIE Fighter"}
        
        result = service.get_vehicle("14")
        
        assert result["name"] == "TIE Fighter"
