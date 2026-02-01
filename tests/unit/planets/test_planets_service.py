from unittest.mock import patch
from app.planets.service import PlanetsService

def test_list_planets():
    with patch('app.planets.service.SWAPIClient') as mock_client:
        service = PlanetsService()
        mock_client.return_value.list_entities.return_value = {"results": [{"name": "Tatooine"}]}
        
        result = service.list_planets()
        
        assert result["results"][0]["name"] == "Tatooine"

def test_get_planet():
    with patch('app.planets.service.SWAPIClient') as mock_client:
        service = PlanetsService()
        mock_client.return_value.get_entity.return_value = {"name": "Alderaan"}
        
        result = service.get_planet("2")
        
        assert result["name"] == "Alderaan"
