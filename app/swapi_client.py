import requests

SWAPI_BASE_URL = "https://swapi.dev/api"

class SWAPIClient:
    @staticmethod
    def get_entity(entity_type: str, entity_id: str) -> dict:
        """
        entity_type can be 'people', 'planets', or 'vehicles'
        """
        # Map entity types if needed, swapi uses 'people', 'planets', 'vehicles'
        # The user mentioned 'vehicle', 'people', 'planets'
        valid_types = ['people', 'planets', 'vehicles']
        if entity_type not in valid_types:
            raise ValueError(f"Invalid entity type: {entity_type}. Must be one of {valid_types}")

        url = f"{SWAPI_BASE_URL}/{entity_type}/{entity_id}/"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                response.raise_for_status()
        except requests.RequestException:
            # For simplicity, we can log this and return None or re-raise
            raise
