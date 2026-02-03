from functools import wraps
from flask import request, jsonify
from app.auth.service import AuthService
from app.user.service import UserService

auth_service = AuthService()
user_service = UserService()

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
        
        user = user_service.get_user_by_id(user_id)
        if not user:
            return jsonify({'message': 'User not found or account disabled!'}), 401
        
        return f(user_id, *args, **kwargs)
    
    return decorated
