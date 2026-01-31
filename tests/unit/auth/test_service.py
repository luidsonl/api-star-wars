import pytest
from app.auth.service import AuthService
import jwt
import os

def test_hash_and_verify_password():
    password = "test_password"
    hashed = AuthService.hash_password(password)
    assert hashed != password
    assert AuthService.verify_password(password, hashed) is True
    assert AuthService.verify_password("wrong_password", hashed) is False

def test_token_generation_and_decoding():
    user_id = "user123"
    token = AuthService.generate_token(user_id)
    assert isinstance(token, str)
    
    decoded_id = AuthService.decode_token(token)
    assert decoded_id == user_id

def test_decode_invalid_token():
    assert AuthService.decode_token("invalid_token") is None
