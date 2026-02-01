from app.swapi_client import SWAPIClient

class PeopleService:
    def __init__(self):
        self.swapi_client = SWAPIClient()

    def list_people(self, page=1, search=None, sort_by=None):
        return self.swapi_client.list_entities('people', page=page, search=search, sort_by=sort_by)

    def get_person(self, person_id):
        return self.swapi_client.get_entity('people', person_id)
