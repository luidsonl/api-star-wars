from flask import Blueprint, request, jsonify
from app.species.service import SpeciesService

species_bp = Blueprint('species', __name__)
species_service = SpeciesService()

@species_bp.route('/', methods=['GET'])
def get_species():
    """
    List Star Wars species
    ---
    tags:
      - Species
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
        description: List of species
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
                $ref: '#/definitions/Species'
    """
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search')
    sort_by = request.args.get('sort_by')
    
    data = species_service.list_species(page=page, search=search, sort_by=sort_by)
    if data:
        return jsonify(data), 200
    return jsonify({"error": "Failed to fetch species"}), 500

@species_bp.route('/<species_id>', methods=['GET'])
def get_specie(species_id):
    """
    Get a specific species
    ---
    tags:
      - Species
    parameters:
      - name: species_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Species details
        schema:
          $ref: '#/definitions/Species'
      404:
        description: Species not found
    definitions:
      Species:
        type: object
        properties:
          name:
            type: string
          classification:
            type: string
          designation:
            type: string
          average_height:
            type: string
          skin_colors:
            type: string
          hair_colors:
            type: string
          eye_colors:
            type: string
          average_lifespan:
            type: string
          homeworld:
            type: string
          language:
            type: string
          people:
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
    data = species_service.get_species(species_id)
    if data:
        return jsonify(data), 200
    return jsonify({"error": "Species not found"}), 404
