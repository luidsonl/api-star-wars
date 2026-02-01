from flask import Blueprint, request, jsonify
from app.people.service import PeopleService

people_bp = Blueprint('people', __name__)
people_service = PeopleService()

@people_bp.route('/', methods=['GET'])
def get_people():
    """
    List Star Wars people
    ---
    tags:
      - People
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
        description: Page number
      - name: search
        in: query
        type: string
        description: Search by name
      - name: sort_by
        in: query
        type: string
        description: Sort by field (e.g., name, height, mass)
    responses:
      200:
        description: List of people
      500:
        description: Internal server error
    """
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search')
    sort_by = request.args.get('sort_by')
    
    data = people_service.list_people(page=page, search=search, sort_by=sort_by)
    if data:
        return jsonify(data), 200
    return jsonify({"error": "Failed to fetch people"}), 500

@people_bp.route('/<person_id>', methods=['GET'])
def get_person(person_id):
    """
    Get a specific person
    ---
    tags:
      - People
    parameters:
      - name: person_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Person details
      404:
        description: Person not found
    """
    data = people_service.get_person(person_id)
    if data:
        return jsonify(data), 200
    return jsonify({"error": "Person not found"}), 404
