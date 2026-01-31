from app.database import db
from app.favorites.model import Favorite
from app.swapi_client import SWAPIClient
from typing import List, Optional

class FavoriteService:
    def __init__(self, database=None):
        self.collection = (database or db).collection('favorites')
        self.swapi_client = SWAPIClient()

    def add_favorite(self, favorite: Favorite) -> str:
        # Check if already exists to avoid duplicates
        existing = self.collection.where('user_id', '==', favorite.user_id)\
                                 .where('entity_type', '==', favorite.entity_type)\
                                 .where('entity_id', '==', favorite.entity_id)\
                                 .limit(1).stream()
        
        for doc in existing:
            return doc.id

        # Validate entity exists in SWAPI
        entity = self.swapi_client.get_entity(favorite.entity_type, favorite.entity_id)
        if not entity:
            raise ValueError(f"Entity {favorite.entity_id} of type {favorite.entity_type} not found in SWAPI")

        _, doc_ref = self.collection.add(favorite.to_dict())
        return doc_ref.id

    def list_favorites(self, user_id: str) -> List[dict]:
        docs = self.collection.where('user_id', '==', user_id).stream()
        favorites = []
        for doc in docs:
            fav = Favorite.from_dict(doc.to_dict(), id=doc.id)
            # Fetch data from SWAPI
            try:
                data = self.swapi_client.get_entity(fav.entity_type, fav.entity_id)
                if data:
                    favorites.append({
                        "id": fav.id,
                        "type": fav.entity_type,
                        "entity_id": fav.entity_id,
                        "data": data
                    })
                else:
                    favorites.append({
                        "id": fav.id,
                        "type": fav.entity_type,
                        "entity_id": fav.entity_id,
                        "error": "Entity no longer exists in SWAPI"
                    })
            except Exception:
                favorites.append({
                    "id": fav.id,
                    "type": fav.entity_type,
                    "entity_id": fav.entity_id,
                    "error": "Failed to fetch data from SWAPI"
                })
        return favorites

    def remove_favorite(self, favorite_id: str, user_id: str) -> bool:
        doc_ref = self.collection.document(favorite_id)
        doc = doc_ref.get()
        if doc.exists and doc.to_dict().get('user_id') == user_id:
            doc_ref.delete()
            return True
        return False
