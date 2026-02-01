from flask import Blueprint, request, jsonify
from app.films.service import FilmsService

films_bp = Blueprint('films', __name__)
films_service = FilmsService()

@films_bp.route('/', methods=['GET'])
def get_films():
    """
    List Star Wars films
    ---
    tags:
      - Films
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
        description: List of films
    """
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search')
    sort_by = request.args.get('sort_by')
    
    data = films_service.list_films(page=page, search=search, sort_by=sort_by)
    if data:
        return jsonify(data), 200
    return jsonify({"error": "Failed to fetch films"}), 500

@films_bp.route('/<film_id>', methods=['GET'])
def get_film(film_id):
    """
    Get a specific film
    ---
    tags:
      - Films
    parameters:
      - name: film_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Film details
      404:
        description: Film not found
    """
    data = films_service.get_film(film_id)
    if data:
        return jsonify(data), 200
    return jsonify({"error": "Film not found"}), 404
