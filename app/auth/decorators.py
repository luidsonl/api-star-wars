from functools import wraps
from flask import request, jsonify
from app.auth.service import AuthService

auth_service = AuthService()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        user_id = auth_service.decode_token(token)
        if not user_id:
            return jsonify({'message': 'Token is invalid or expired!'}), 401
        
        return f(user_id, *args, **kwargs)
    
    return decorated
