from unittest.mock import patch
from app.species.service import SpeciesService

def test_list_species():
    with patch('app.species.service.SWAPIClient') as mock_client:
        service = SpeciesService()
        mock_client.return_value.list_entities.return_value = {"results": [{"name": "Wookie"}]}
        
        result = service.list_species()
        
        assert result["results"][0]["name"] == "Wookie"

def test_get_species():
    with patch('app.species.service.SWAPIClient') as mock_client:
        service = SpeciesService()
        mock_client.return_value.get_entity.return_value = {"name": "Ewok"}
        
        result = service.get_species("3")
        
        assert result["name"] == "Ewok"
