from app.swapi_client import SWAPIClient

class VehiclesService:
    def __init__(self):
        self.swapi_client = SWAPIClient()

    def list_vehicles(self, page=1, search=None, sort_by=None):
        return self.swapi_client.list_entities('vehicles', page=page, search=search, sort_by=sort_by)

    def get_vehicle(self, vehicle_id):
        return self.swapi_client.get_entity('vehicles', vehicle_id)
