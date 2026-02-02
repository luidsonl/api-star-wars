import hashlib
from datetime import datetime, timezone
from app.database.core import db

class SWAPICacheRepository:
    def __init__(self, database=None):
        self.collection = (database or db).collection('swapi_cache')

    def _get_url_hash(self, url: str) -> str:
        """Gera um hash SHA-256 da URL para usar como ID do documento."""
        return hashlib.sha256(url.encode('utf-8')).hexdigest()

    def get_cached_response(self, url: str) -> dict:
        """Recupera uma resposta em cache pela URL. Retorna None se não encontrada."""
        doc_id = self._get_url_hash(url)
        doc_ref = self.collection.document(doc_id)
        doc = doc_ref.get()
        
        if doc.exists:
            return doc.to_dict().get('data')
        return None

    def cache_response(self, url: str, data: dict):
        """Armazena uma resposta da SWAPI no cache."""
        doc_id = self._get_url_hash(url)
        doc_ref = self.collection.document(doc_id)
        
        cache_data = {
            'url': url,
            'data': data,
            'created_at': datetime.now(timezone.utc)
        }
        
        doc_ref.set(cache_data)
