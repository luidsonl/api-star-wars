import jwt
import datetime
import os
from passlib.hash import bcrypt
from typing import Optional

# In production, this should be set in environment variables
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "star-wars-secret-key-123")

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hash(password)

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        return bcrypt.verify(password, hashed)

    @staticmethod
    def generate_token(user_id: str) -> str:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    @staticmethod
    def decode_token(token: str) -> Optional[str]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return payload['sub']
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None
