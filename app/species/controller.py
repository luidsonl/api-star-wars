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
      404:
        description: Species not found
    """
    data = species_service.get_species(species_id)
    if data:
        return jsonify(data), 200
    return jsonify({"error": "Species not found"}), 404
