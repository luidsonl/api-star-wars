from unittest.mock import patch

def test_get_films(client):
    with patch('app.films.controller.films_service') as mock_service:
        mock_service.list_films.return_value = {"results": [{"title": "A New Hope"}]}
        
        response = client.get('/films/')
        
        assert response.status_code == 200
        assert response.json['results'][0]['title'] == "A New Hope"

def test_get_film(client):
    with patch('app.films.controller.films_service') as mock_service:
        mock_service.get_film.return_value = {"title": "A New Hope"}
        
        response = client.get('/films/1')
        
        assert response.status_code == 200
        assert response.json['title'] == "A New Hope"
