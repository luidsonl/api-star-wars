from flask import Blueprint, request, jsonify
from app.favorites.service import FavoriteService
from app.favorites.model import Favorite
from app.auth.decorators import token_required
from pydantic import ValidationError
from app.favorites.dto.favorite_dto import FavoriteCreateDTO

favorites_bp = Blueprint('favorites', __name__)
favorite_service = FavoriteService()

@favorites_bp.route('/', methods=['GET'])
@token_required
def get_favorites(user_id):
    favorites = favorite_service.list_favorites(user_id)
    return jsonify(favorites), 200

@favorites_bp.route('/', methods=['POST'])
@token_required
def add_favorite(user_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        dto = FavoriteCreateDTO(**data)
        
        favorite = Favorite(
            id=None,
            user_id=user_id,
            entity_type=dto.entity_type,
            entity_id=dto.entity_id
        )
        
        fav_id = favorite_service.add_favorite(favorite)
        return jsonify({"id": fav_id, "message": "Favorite added"}), 201
    except ValidationError as e:
        return jsonify(e.errors()), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@favorites_bp.route('/<favorite_id>', methods=['DELETE'])
@token_required
def delete_favorite(user_id, favorite_id):
    try:
        success = favorite_service.remove_favorite(favorite_id, user_id)
        if success:
            return jsonify({"message": "Favorite removed"}), 200
        return jsonify({"error": "Favorite not found or not owned by user"}), 404
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
