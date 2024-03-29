from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from init import db
from models.transportation import Transportation, TransportationSchema
from datetime import datetime
from models.trips import Trip
from models.transportType import TransportType

transport_bp = Blueprint('transport_controller', __name__, url_prefix='/transport')

transport_schema = TransportationSchema()
transports_schema = TransportationSchema(many=True)

# Create a transportation entry
@transport_bp.route('/create', methods=['POST'])
@jwt_required()
def create_transport():
    trip_id = request.json.get('trip_id')
    transport_type_id = request.json.get('transport_type_id')
    arrival_time = datetime.strptime(request.json.get('arrival_time'), '%Y-%m-%d %H:%M:%S')  
    departure_time = datetime.strptime(request.json.get('departure_time'), '%Y-%m-%d %H:%M:%S')  
    arrival_location = request.json.get('arrival_location')
    departure_location = request.json.get('departure_location')
    cost = request.json.get('cost')

    if not all([trip_id, transport_type_id, arrival_time, departure_time, arrival_location, departure_location, cost]):
        return jsonify({'error': 'Missing required fields.'}), 400
    
    # Ensure trip_id and transport_type_id are valid
    if not (Trip.query.get(trip_id) and TransportType.query.get(transport_type_id)):
        return jsonify({'error': 'Invalid trip_id or transport_type_id. Reminder: transport type must be between 1-8'}), 400
    
    try:
        arrival_time = datetime.strptime(arrival_time, '%Y-%m-%d %H:%M:%S')
        departure_time = datetime.strptime(departure_time, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'error': 'Invalid datetime format. Please provide datetime in YYYY-MM-DD HH:MM:SS format.'}), 400

    new_transport = Transportation(
        trip_id=trip_id,
        transport_type_id=transport_type_id,
        arrival_time=arrival_time,
        departure_time=departure_time,
        arrival_location=arrival_location,
        departure_location=departure_location,
        cost=cost
    )

    db.session.add(new_transport)
    db.session.commit()

    return jsonify(transport_schema.dump(new_transport))

# Get all transportation entries
@transport_bp.route('/read', methods=['GET'])
@jwt_required()
def get_transports():
    all_transports = Transportation.query.all()
    result = transports_schema.dump(all_transports)
    return jsonify(result)

# Get single transportation entry by ID
@transport_bp.route('/read/<int:id>', methods=['GET'])
@jwt_required()
def get_transport(id):
    transport = Transportation.query.get(id)
    if not transport:
        return jsonify({'error': 'Transportation not found.'}), 404
    return jsonify(transport_schema.dump(transport))

# Update a transportation entry
@transport_bp.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_transport(id):
    transport = Transportation.query.get(id)

    # If transportation entry doesn't exist, return 404
    if not transport:
        return jsonify({'error': 'Transportation not found.'}), 404 

    # Update transportation fields if provided in request
    for key, value in request.json.items():
        if hasattr(transport, key):
            setattr(transport, key, value)

    db.session.commit()

    # Return the updated transportation entry
    return jsonify(transport_schema.dump(transport))

# Delete a transportation entry
@transport_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_transport(id):
    transport = Transportation.query.get(id)

    # If transportation entry doesn't exist, return 404
    if not transport:
        return jsonify({'error': 'Transportation not found.'}), 404

    db.session.delete(transport)
    db.session.commit()

    return jsonify({'message': f'Transportation with ID {id} deleted successfully.'})
