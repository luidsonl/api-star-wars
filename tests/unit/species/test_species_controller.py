from unittest.mock import patch

def test_get_species(client):
    with patch('app.species.controller.species_service') as mock_service:
        mock_service.list_species.return_value = {"results": [{"name": "Wookie"}]}
        
        response = client.get('/species/')
        
        assert response.status_code == 200
        assert response.json['results'][0]['name'] == "Wookie"

def test_get_specie_detail(client):
    with patch('app.species.controller.species_service') as mock_service:
        mock_service.get_species.return_value = {"name": "Wookie"}
        
        response = client.get('/species/1')
        
        assert response.status_code == 200
        assert response.json['name'] == "Wookie"
