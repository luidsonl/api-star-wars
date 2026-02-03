import jwt
import datetime
import os
from passlib.hash import bcrypt
from typing import Optional

# In production, this should be set in environment variables
# Minimum length for HS256 should be 32 bytes
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "star-wars-super-secret-key-that-is-at-least-32-chars-long")

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hash(password)

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        return bcrypt.verify(password, hashed)

    @staticmethod
    def generate_token(user_id: str) -> str:
        now = datetime.datetime.now(datetime.timezone.utc)
        payload = {
            'exp': now + datetime.timedelta(days=1),
            'iat': now,
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
