from flask import Blueprint, request, jsonify
from app.auth.service import AuthService
from app.user.service import UserService
from app.user.model import User
from pydantic import ValidationError
from app.user.dto.user_dto import UserCreateDTO, UserLoginDTO

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()
user_service = UserService()

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        dto = UserCreateDTO(**data)
        
        # Hash password
        hashed_password = auth_service.hash_password(dto.password)
        
        # Create user
        new_user = User(
            id=None,
            email=dto.email,
            password_hash=hashed_password,
            name=dto.name
        )
        
        user_id = user_service.create_user(new_user)
        return jsonify({"id": user_id, "message": "User created successfully"}), 201
    except ValidationError as e:
        return jsonify(e.errors()), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        dto = UserLoginDTO(**data)
        
        user = user_service.get_user_by_email(dto.email)
        if not user or not auth_service.verify_password(dto.password, user.password_hash):
            return jsonify({"error": "Invalid email or password"}), 401
        
        token = auth_service.generate_token(user.id)
        return jsonify({"token": token}), 200
    except ValidationError as e:
        return jsonify(e.errors()), 400
