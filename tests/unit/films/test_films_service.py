from unittest.mock import patch
from app.films.service import FilmsService

def test_list_films():
    with patch('app.films.service.SWAPIClient') as mock_client:
        service = FilmsService()
        mock_client.return_value.list_entities.return_value = {"results": [{"title": "A New Hope"}]}
        
        result = service.list_films(page=1)
        
        mock_client.return_value.list_entities.assert_called_once_with('films', page=1, search=None, sort_by=None)
        assert result["results"][0]["title"] == "A New Hope"

def test_get_film():
    with patch('app.films.service.SWAPIClient') as mock_client:
        service = FilmsService()
        mock_client.return_value.get_entity.return_value = {"title": "The Empire Strikes Back"}
        
        result = service.get_film("2")
        
        mock_client.return_value.get_entity.assert_called_once_with('films', "2")
        assert result["title"] == "The Empire Strikes Back"
