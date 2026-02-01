import requests
from app.database.swapi_cache_repo import SWAPICacheRepository

SWAPI_BASE_URL = "https://swapi.dev/api"

class SWAPIClient:
    def __init__(self, database=None):
        self.cache_repo = SWAPICacheRepository(database=database)

    def get_by_url(self, url: str) -> dict:
        """
        Generic method to fetch data from any SWAPI URL, with caching.
        """
        # Ensure trailing slash for swapi.dev consistency if it's an entity URL
        if not url.endswith('/') and '?' not in url:
            url += '/'

        # Check cache first
        cached_data = self.cache_repo.get_cached_response(url)
        if cached_data:
            return cached_data

        # Cache miss: Fetch from API
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                # Store in cache
                self.cache_repo.cache_response(url, data)
                return data
            return None
        except requests.RequestException:
            return None

    def get_entity(self, entity_type: str, entity_id: str) -> dict:
        """
        Get a specific entity by type and ID.
        entity_type can be 'people', 'planets', or 'vehicles'
        """
        valid_types = ['people', 'planets', 'vehicles']
        if entity_type not in valid_types:
            raise ValueError(f"Invalid entity type: {entity_type}. Must be one of {valid_types}")

        url = f"{SWAPI_BASE_URL}/{entity_type}/{entity_id}/"
        return self.get_by_url(url)

    def list_entities(self, entity_type: str, page: int = 1, search: str = None) -> dict:
        """
        List entities with support for pagination and search.
        """
        valid_types = ['people', 'planets', 'vehicles']
        if entity_type not in valid_types:
            raise ValueError(f"Invalid entity type: {entity_type}. Must be one of {valid_types}")

        url = f"{SWAPI_BASE_URL}/{entity_type}/?page={page}"
        if search:
            url += f"&search={search}"

        return self.get_by_url(url)
