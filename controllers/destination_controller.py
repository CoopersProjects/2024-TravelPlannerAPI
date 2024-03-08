from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from init import db
from models.destination import Destination, DestinationSchema

destination_bp = Blueprint('destination_controller', __name__, url_prefix='/destination')

destination_schema = DestinationSchema()
destinations_schema = DestinationSchema(many=True)

# Create a destination
@destination_bp.route('/create', methods=['POST'])
@jwt_required()
def create_destination():
    name = request.json.get('name')
    description = request.json.get('description')
    location = request.json.get('location')
    climate_id = request.json.get('climate_id')

    if not all([name, location, climate_id]):
        return jsonify({'error': 'Missing required fields.'}), 400
    
    climate_id = int(request.json.get('climate_id'))
    
    if not 1 <= climate_id <= 5:
        return jsonify({'error': 'Invalid climate_id. Must be between 1 and 5.'}), 400

    new_destination = Destination(name=name, description=description, location=location, climate_id=climate_id)

    db.session.add(new_destination)
    db.session.commit()

    return jsonify(destination_schema.dump(new_destination)), 201

# Get all destinations
@destination_bp.route('/read', methods=['GET'])
def get_destinations():
    all_destinations = Destination.query.all()
    result = destinations_schema.dump(all_destinations)
    return jsonify(result)

# Get single destination by ID
@destination_bp.route('/read/<int:id>', methods=['GET'])
def get_destination(id):
    destination = Destination.query.get(id)
    if not destination:
        return jsonify({'error': 'Destination not found.'}), 404
    return jsonify(destination_schema.dump(destination))

# Update a destination
@destination_bp.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_destination(id):
    destination = Destination.query.get(id)

    if not destination:
        return jsonify({'error': 'Destination not found.'}), 404

    name = request.json.get('name')
    description = request.json.get('description')
    location = request.json.get('location')
    climate_id = request.json.get('climate_id')

    destination.name = name
    destination.description = description
    destination.location = location
    destination.climate_id = climate_id

    climate_id = int(request.json.get('climate_id'))

    if not 1 <= climate_id <= 5:
        return jsonify({'error': 'Invalid climate_id. Must be between 1 and 5.'}), 400

    db.session.commit()

    return jsonify(destination_schema.dump(destination))

# Delete a destination
@destination_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_destination(id):
    destination = Destination.query.get(id)

    if not destination:
        return jsonify({'error': 'Destination not found.'}), 404

    db.session.delete(destination)
    db.session.commit()

    return jsonify({'message': f'Successfully deleted destination with id {id}'}), 200
