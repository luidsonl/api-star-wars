from app.swapi_client import SWAPIClient

class FilmsService:
    def __init__(self):
        self.swapi_client = SWAPIClient()

    def list_films(self, page=1, search=None, sort_by=None):
        return self.swapi_client.list_entities('films', page=page, search=search, sort_by=sort_by)

    def get_film(self, film_id):
        return self.swapi_client.get_entity('films', film_id)
