from flask import Blueprint, request, jsonify
from app.starships.service import StarshipsService

starships_bp = Blueprint('starships', __name__)
starships_service = StarshipsService()

@starships_bp.route('/', methods=['GET'])
def get_starships():
    """
    List Star Wars starships
    ---
    tags:
      - Starships
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: search
        in: query
        type: string
      - name: sort_by
        in: query
        type: string
    responses:
      200:
        description: List of starships
    """
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search')
    sort_by = request.args.get('sort_by')
    
    data = starships_service.list_starships(page=page, search=search, sort_by=sort_by)
    if data:
        return jsonify(data), 200
    return jsonify({"error": "Failed to fetch starships"}), 500

@starships_bp.route('/<starship_id>', methods=['GET'])
def get_starship(starship_id):
    """
    Get a specific starship
    ---
    tags:
      - Starships
    parameters:
      - name: starship_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Starship details
      404:
        description: Starship not found
    """
    data = starships_service.get_starship(starship_id)
    if data:
        return jsonify(data), 200
    return jsonify({"error": "Starship not found"}), 404
