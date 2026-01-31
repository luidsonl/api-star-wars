from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class User:
    id: Optional[str]
    email: str
    password_hash: str
    name: str

    def to_dict(self):
        d = asdict(self)
        if 'id' in d:
            del d['id']
        return d

    @classmethod
    def from_dict(cls, data: dict, id: Optional[str] = None):
        return cls(
            id=id,
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            name=data.get('name')
        )
