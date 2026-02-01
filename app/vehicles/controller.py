from flask import Blueprint, request, jsonify
from app.vehicles.service import VehiclesService

vehicles_bp = Blueprint('vehicles', __name__)
vehicles_service = VehiclesService()

@vehicles_bp.route('/', methods=['GET'])
def get_vehicles():
    """
    List Star Wars vehicles
    ---
    tags:
      - Vehicles
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
        description: List of vehicles
    """
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search')
    sort_by = request.args.get('sort_by')
    
    data = vehicles_service.list_vehicles(page=page, search=search, sort_by=sort_by)
    if data:
        return jsonify(data), 200
    return jsonify({"error": "Failed to fetch vehicles"}), 500

@vehicles_bp.route('/<vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    """
    Get a specific vehicle
    ---
    tags:
      - Vehicles
    parameters:
      - name: vehicle_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Vehicle details
      404:
        description: Vehicle not found
    """
    data = vehicles_service.get_vehicle(vehicle_id)
    if data:
        return jsonify(data), 200
    return jsonify({"error": "Vehicle not found"}), 404
