from pydantic import BaseModel
from typing import Literal

class FavoriteCreateDTO(BaseModel):
    entity_type: Literal['people', 'planets', 'vehicles']
    entity_id: str
