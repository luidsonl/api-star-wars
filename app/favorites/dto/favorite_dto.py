from pydantic import BaseModel
from typing import Literal

class FavoriteCreateDTO(BaseModel):
    entity_type: Literal['people', 'planets', 'vehicles', 'films', 'species', 'starships']
    entity_id: str
