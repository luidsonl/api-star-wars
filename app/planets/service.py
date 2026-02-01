from app.swapi_client import SWAPIClient

class PlanetsService:
    def __init__(self):
        self.swapi_client = SWAPIClient()

    def list_planets(self, page=1, search=None, sort_by=None):
        return self.swapi_client.list_entities('planets', page=page, search=search, sort_by=sort_by)

    def get_planet(self, planet_id):
        return self.swapi_client.get_entity('planets', planet_id)
