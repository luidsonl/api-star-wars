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
        schema:
          properties:
            count:
              type: integer
            next:
              type: string
            previous:
              type: string
            results:
              type: array
              items:
                $ref: '#/definitions/Starship'
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
        schema:
          $ref: '#/definitions/Starship'
      404:
        description: Starship not found
    definitions:
      Starship:
        type: object
        properties:
          name:
            type: string
          model:
            type: string
          manufacturer:
            type: string
          cost_in_credits:
            type: string
          length:
            type: string
          max_atmosphering_speed:
            type: string
          crew:
            type: string
          passengers:
            type: string
          cargo_capacity:
            type: string
          consumables:
            type: string
          hyperdrive_rating:
            type: string
          MGLT:
            type: string
          starship_class:
            type: string
          pilots:
            type: array
            items:
              type: string
          films:
            type: array
            items:
              type: string
          created:
            type: string
          edited:
            type: string
          url:
            type: string
    """
    data = starships_service.get_starship(starship_id)
    if data:
        return jsonify(data), 200
    return jsonify({"error": "Starship not found"}), 404
