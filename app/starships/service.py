from app.swapi_client import SWAPIClient

class StarshipsService:
    def __init__(self):
        self.swapi_client = SWAPIClient()

    def list_starships(self, page=1, search=None, sort_by=None):
        return self.swapi_client.list_entities('starships', page=page, search=search, sort_by=sort_by)

    def get_starship(self, starship_id):
        return self.swapi_client.get_entity('starships', starship_id)
