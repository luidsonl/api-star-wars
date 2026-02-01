from app.swapi_client import SWAPIClient

class SpeciesService:
    def __init__(self):
        self.swapi_client = SWAPIClient()

    def list_species(self, page=1, search=None, sort_by=None):
        return self.swapi_client.list_entities('species', page=page, search=search, sort_by=sort_by)

    def get_species(self, species_id):
        return self.swapi_client.get_entity('species', species_id)
