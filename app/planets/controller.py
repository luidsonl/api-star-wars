from flask import Blueprint, request, jsonify
from app.planets.service import PlanetsService

planets_bp = Blueprint('planets', __name__)
planets_service = PlanetsService()

@planets_bp.route('/', methods=['GET'])
def get_planets():
    """
    List Star Wars planets
    ---
    tags:
      - Planets
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
        description: List of planets
    """
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search')
    sort_by = request.args.get('sort_by')
    
    data = planets_service.list_planets(page=page, search=search, sort_by=sort_by)
    if data:
        return jsonify(data), 200
    return jsonify({"error": "Failed to fetch planets"}), 500

@planets_bp.route('/<planet_id>', methods=['GET'])
def get_planet(planet_id):
    """
    Get a specific planet
    ---
    tags:
      - Planets
    parameters:
      - name: planet_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Planet details
      404:
        description: Planet not found
    """
    data = planets_service.get_planet(planet_id)
    if data:
        return jsonify(data), 200
    return jsonify({"error": "Planet not found"}), 404
