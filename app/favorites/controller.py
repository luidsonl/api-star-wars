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
    """
    List user favorites
    ---
    tags:
      - Favorites
    security:
      - Bearer: []
    responses:
      200:
        description: List of favorites
        schema:
          type: array
          items:
            $ref: '#/definitions/Favorite'
      401:
        description: Unauthorized
    """
    favorites = favorite_service.list_favorites(user_id)
    return jsonify(favorites), 200

@favorites_bp.route('/', methods=['POST'])
@token_required
def add_favorite(user_id):
    """
    Add a new favorite
    ---
    tags:
      - Favorites
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/FavoriteCreate'
    responses:
      201:
        description: Favorite added
        schema:
          properties:
            id:
              type: string
            message:
              type: string
      400:
        description: Invalid input
      401:
        description: Unauthorized
    """
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

@favorites_bp.route('/<favorite_id>', methods=['DELETE'])
@token_required
def delete_favorite(user_id, favorite_id):
    """
    Delete a favorite
    ---
    tags:
      - Favorites
    security:
      - Bearer: []
    parameters:
      - name: favorite_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Favorite removed
        schema:
          properties:
            message:
              type: string
      401:
        description: Unauthorized
      404:
        description: Favorite not found or not owned by user
    definitions:
      Favorite:
        type: object
        properties:
          id:
            type: string
          entity_type:
            type: string
            enum: ['people', 'planets', 'vehicles', 'films', 'species', 'starships']
          entity_id:
            type: string
      FavoriteCreate:
        type: object
        required:
          - entity_type
          - entity_id
        properties:
          entity_type:
            type: string
            enum: ['people', 'planets', 'vehicles', 'films', 'species', 'starships']
          entity_id:
            type: string
    """
    success = favorite_service.remove_favorite(favorite_id, user_id)
    if success:
        return jsonify({"message": "Favorite removed"}), 200
    return jsonify({"error": "Favorite not found or not owned by user"}), 404
