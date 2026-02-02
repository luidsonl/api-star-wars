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
        Método genérico para buscar dados de qualquer URL da SWAPI, com cache.
        """
        # Certifica que a URL termina com / se não tiver ?
        if not url.endswith('/') and '?' not in url:
            url += '/'

        # Verifica o cache primeiro
        cached_data = self.cache_repo.get_cached_response(url)
        if cached_data:
            return self._substitute_urls(cached_data) if substitute else cached_data

        # Cache miss: Busca na API
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                # Armazena no cache
                self.cache_repo.cache_response(url, data)
                
                # Substitui URLs na resposta
                return self._substitute_urls(data) if substitute else data
            return None
        except requests.RequestException:
            return None

    def _substitute_urls(self, data):
        """
        Substitui recursivamente SWAPI_BASE_URL pelo URL base atual ou o torna relativo.
        """
        if not data:
            return data

        # Determina a URL base
        if has_request_context():
            # Se estivermos em um contexto de requisição, usa o url_root (ex: http://localhost:8080/prefix/)
            target_base = request.url_root.rstrip('/')
        else:
            # Fallback para contextos sem requisição (ex: testes, scripts)
            target_base = ""

        def _replace(val):
            if isinstance(val, str) and val.startswith(SWAPI_BASE_URL):
                # Substitui SWAPI_BASE_URL por target_base
                # Precisamos lidar com o caso em que target_base está vazio (URLs relativas)
                path = val[len(SWAPI_BASE_URL):]
                if target_base:
                    return f"{target_base}{path}"
                return path.lstrip('/') # Retorna caminho relativo
            elif isinstance(val, list):
                return [_replace(i) for i in val]
            elif isinstance(val, dict):
                return {k: _replace(v) for k, v in val.items()}
            return val

        return _replace(data)

    def get_entity(self, entity_type: str, entity_id: str) -> dict:
        """
        Pega uma entidade específica por tipo e ID.
        """
        if entity_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid entity type: {entity_type}. Must be one of {self.VALID_TYPES}")

        url = f"{SWAPI_BASE_URL}/{entity_type}/{entity_id}/"
        return self.get_by_url(url)

    def get_all_entities(self, entity_type: str) -> list:
        """
        Busca todas as entidades de um determinado tipo percorrendo todas as páginas.
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
        """Helper para converter valores SWAPI como '172' ou '77' para float para ordenação."""
        if value is None or value in ['unknown', 'n/a', 'none']:
            return float('-inf')  # Coloca valores desconhecidos no final (ou início dependendo da ordem)
        try:
            # Lida com valores como "1,000" ou "unknown"
            clean_value = str(value).replace(',', '')
            return float(clean_value)
        except ValueError:
            return value # Return as is for string comparison

    def list_entities(self, entity_type: str, page: int = 1, search: str = None, sort_by: str = None) -> dict:
        """
        Lista entidades com suporte a paginação, busca e ordenação.
        Se sort_by for fornecido, busca todas as entidades para realizar a ordenação.
        """
        if entity_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid entity type: {entity_type}. Must be one of {self.VALID_TYPES}")

        if sort_by:
            results = self.get_all_entities(entity_type)
            
            # Aplica busca se fornecida
            if search:
                search = search.lower()
                results = [r for r in results if search in str(r.get('name', r.get('title', ''))).lower()]

            # Aplica ordenação
            if results and sort_by in results[0]:
                results.sort(key=lambda x: self._parse_numeric(x.get(sort_by)))

            # Pagina os resultados ordenados manualmente
            page_size = 10
            start = (page - 1) * page_size
            end = start + page_size
            
            # Constrói URLs completas para os links next/previous para que possam ser substituídas corretamente
            next_url = None
            if end < len(results):
                next_url = f"{SWAPI_BASE_URL}/{entity_type}/?page={page + 1}"
                if search:
                    next_url += f"&search={search}"
                next_url += f"&sort_by={sort_by}"

            prev_url = None
            if start > 0:
                prev_url = f"{SWAPI_BASE_URL}/{entity_type}/?page={page - 1}"
                if search:
                    prev_url += f"&search={search}"
                prev_url += f"&sort_by={sort_by}"

            data = {
                "count": len(results),
                "next": next_url,
                "previous": prev_url,
                "results": results[start:end]
            }
            return self._substitute_urls(data)

        # Paginação padrão (server-side)
        url = f"{SWAPI_BASE_URL}/{entity_type}/?page={page}"
        if search:
            url += f"&search={search}"

        return self.get_by_url(url)

