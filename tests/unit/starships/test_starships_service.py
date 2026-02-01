from unittest.mock import patch
from app.starships.service import StarshipsService

def test_list_starships():
    with patch('app.starships.service.SWAPIClient') as mock_client:
        service = StarshipsService()
        mock_client.return_value.list_entities.return_value = {"results": [{"name": "Millennium Falcon"}]}
        
        result = service.list_starships()
        
        assert result["results"][0]["name"] == "Millennium Falcon"

def test_get_starship():
    with patch('app.starships.service.SWAPIClient') as mock_client:
        service = StarshipsService()
        mock_client.return_value.get_entity.return_value = {"name": "X-wing"}
        
        result = service.get_starship("12")
        
        assert result["name"] == "X-wing"
