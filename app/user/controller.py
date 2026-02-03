from flask import Blueprint, jsonify
from app.user.service import UserService
from app.auth.decorators import token_required

user_bp = Blueprint('user', __name__)
user_service = UserService()

@user_bp.route('/me', methods=['GET'])
@token_required
def get_me(user_id):
    """
    Get current user profile
    ---
    tags:
      - Users
    security:
      - Bearer: []
    responses:
      200:
        description: User profile details
        schema:
          $ref: '#/definitions/UserProfile'
      401:
        description: Unauthorized - Token missing or invalid
      404:
        description: User not found
    definitions:
      UserProfile:
        type: object
        properties:
          id:
            type: string
          email:
            type: string
          name:
            type: string
    """
    user = user_service.get_user_by_id(user_id)
    if user:
        return jsonify({
            "id": user.id,
            "email": user.email,
            "name": user.name
        }), 200
    return jsonify({"error": "User not found"}), 404
