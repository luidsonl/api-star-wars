import requests
from flask import request, has_request_context
from app.database.swapi_cache_repo import SWAPICacheRepository

SWAPI_BASE_URL = "https://swapi.dev/api"

class SWAPIClient:
    VALID_TYPES = ['people', 'planets', 'vehicles', 'films', 'species', 'starships']

    def __init__(self, database=None):
        self.cache_repo = SWAPICacheRepository(database=database)

    def get_by_url(self, url: str, substitute: bool = True) -> dict:
        """
        Generic method to fetch data from any SWAPI URL, with caching.
        """
        # Ensure trailing slash for swapi.dev consistency if it's an entity URL
        if not url.endswith('/') and '?' not in url:
            url += '/'

        # Check cache first
        cached_data = self.cache_repo.get_cached_response(url)
        if cached_data:
            return self._substitute_urls(cached_data) if substitute else cached_data

        # Cache miss: Fetch from API
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                # Store in cache
                self.cache_repo.cache_response(url, data)
                
                # Substitute URLs in the response
                return self._substitute_urls(data) if substitute else data
            return None
        except requests.RequestException:
            return None

    def _substitute_urls(self, data):
        """
        Recursively replaces SWAPI_BASE_URL with the current host URL or makes it relative.
        """
        if not data:
            return data

        # Determine target base URL
        if has_request_context():
            # If we are in a request context, use the url_root (e.g., http://localhost:8080/prefix/)
            target_base = request.url_root.rstrip('/')
        else:
            # Fallback for non-request contexts (e.g., tests, scripts)
            target_base = ""

        def _replace(val):
            if isinstance(val, str) and val.startswith(SWAPI_BASE_URL):
                # Replace SWAPI_BASE_URL with target_base
                # We need to handle the case where target_base is empty (relative URLs)
                path = val[len(SWAPI_BASE_URL):]
                if target_base:
                    return f"{target_base}{path}"
                return path.lstrip('/') # Return relative path
            elif isinstance(val, list):
                return [_replace(i) for i in val]
            elif isinstance(val, dict):
                return {k: _replace(v) for k, v in val.items()}
            return val

        return _replace(data)

    def get_entity(self, entity_type: str, entity_id: str) -> dict:
        """
        Get a specific entity by type and ID.
        """
        if entity_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid entity type: {entity_type}. Must be one of {self.VALID_TYPES}")

        url = f"{SWAPI_BASE_URL}/{entity_type}/{entity_id}/"
        return self.get_by_url(url)

    def get_all_entities(self, entity_type: str) -> list:
        """
        Fetch all entities of a given type by traversing all pages.
        """
        if entity_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid entity type: {entity_type}")

        all_results = []
        url = f"{SWAPI_BASE_URL}/{entity_type}/"
        
        while url:
            data = self.get_by_url(url, substitute=False)
            if not data:
                break
            all_results.extend(data.get("results", []))
            url = data.get("next")
            
        return all_results

    def _parse_numeric(self, value):
        """Helper to parse SWAPI values like '172' or '77' to float for sorting."""
        if value is None or value in ['unknown', 'n/a', 'none']:
            return float('-inf')  # Put unknown values at the end (or beginning depending on order)
        try:
            # Handle values like "1,000" or "unknown"
            clean_value = str(value).replace(',', '')
            return float(clean_value)
        except ValueError:
            return value # Return as is for string comparison

    def list_entities(self, entity_type: str, page: int = 1, search: str = None, sort_by: str = None) -> dict:
        """
        List entities with support for pagination, search, and sorting.
        If sort_by is provided, fetches all entities to perform sorting.
        """
        if entity_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid entity type: {entity_type}. Must be one of {self.VALID_TYPES}")

        if sort_by:
            results = self.get_all_entities(entity_type)
            
            # Apply search if provided
            if search:
                search = search.lower()
                results = [r for r in results if search in str(r.get('name', r.get('title', ''))).lower()]

            # Apply sorting
            if results and sort_by in results[0]:
                results.sort(key=lambda x: self._parse_numeric(x.get(sort_by)))

            # Paginate the sorted results manually
            page_size = 10
            start = (page - 1) * page_size
            end = start + page_size
            
            data = {
                "count": len(results),
                "next": f"page={page + 1}" if end < len(results) else None,
                "previous": f"page={page - 1}" if start > 0 else None,
                "results": results[start:end]
            }
            return self._substitute_urls(data)

        # Standard pagination (server-side)
        url = f"{SWAPI_BASE_URL}/{entity_type}/?page={page}"
        if search:
            url += f"&search={search}"

        return self.get_by_url(url)

