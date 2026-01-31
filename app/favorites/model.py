from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Favorite:
    id: Optional[str]
    user_id: str
    entity_type: str  # 'people', 'planets', 'vehicles'
    entity_id: str

    def to_dict(self):
        d = asdict(self)
        if 'id' in d:
            del d['id']
        return d

    @classmethod
    def from_dict(cls, data: dict, id: Optional[str] = None):
        return cls(
            id=id,
            user_id=data.get('user_id'),
            entity_type=data.get('entity_type'),
            entity_id=data.get('entity_id')
        )
