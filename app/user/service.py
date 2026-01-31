from app.database import db
from app.user.model import User
from typing import Optional

class UserService:
    def __init__(self, database=None):
        self.collection = (database or db).collection('users')

    def create_user(self, user: User) -> str:
        # Check if user already exists
        if self.get_user_by_email(user.email):
            raise ValueError("User already exists")
        
        _, doc_ref = self.collection.add(user.to_dict())
        return doc_ref.id

    def get_user_by_email(self, email: str) -> Optional[User]:
        docs = self.collection.where('email', '==', email).limit(1).stream()
        for doc in docs:
            return User.from_dict(doc.to_dict(), id=doc.id)
        return None

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        doc = self.collection.document(user_id).get()
        if doc.exists:
            return User.from_dict(doc.to_dict(), id=doc.id)
        return None
