from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from init import db
from models.accomodation import Accommodation, AccommodationSchema
from models.trips import Trip
from datetime import datetime

accom_bp = Blueprint('accommodation_controller', __name__, url_prefix='/accommodation')

accommodation_schema = AccommodationSchema()
accommodations_schema = AccommodationSchema(many=True)

# Create an accommodation associated with a trip
@accom_bp.route('/create', methods=['POST'])
@jwt_required()
def create_accommodation():
    data = request.json
    name = data.get('name')
    address = data.get('address')
    check_in = datetime.strptime(data.get('check_in'), '%Y-%m-%d') if data.get('check_in') else None
    check_out = datetime.strptime(data.get('check_out'), '%Y-%m-%d') if data.get('check_out') else None
    cost_per_night = data.get('cost_per_night')
    trip_id = data.get('trip_id')

    if not all([name, address, cost_per_night, trip_id]):
        return jsonify({'error': 'Missing required fields.'}), 400

    # Check if the trip ID exists in the database
    if not Trip.query.get(trip_id):
        return jsonify({'error': 'Trip with the provided ID does not exist.'}), 404

    new_accommodation = Accommodation(
        name=name,
        address=address,
        check_in=check_in,
        check_out=check_out,
        cost_per_night=cost_per_night,
        trip_id=trip_id
    )

    db.session.add(new_accommodation)
    db.session.commit()

    return jsonify(accommodation_schema.dump(new_accommodation))

@accom_bp.route('/read', methods=['GET'])
def get_all_accommodations():
    accommodations = Accommodation.query.all()
    # Serialize the accommodations data using the schema
    result = accommodations_schema.dump(accommodations)
    # Return the JSON response
    return jsonify(result)

@accom_bp.route('/read/<int:id>', methods=['GET'])
def get_accommodation_by_id(id):
    accommodation = Accommodation.query.get(id)
    if not accommodation:
        return jsonify({'error': 'Accommodation not found.'}), 404
    return jsonify(accommodation_schema.dump(accommodation))

# Update an accommodation
@accom_bp.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_accommodation(id):
    accommodation = Accommodation.query.get(id)
    if not accommodation:
        return jsonify({'error': 'Accommodation not found.'}), 404

    data = request.json
    trip_id = data.get('trip_id')

    # Check if the new trip ID exists in the database
    if trip_id and not Trip.query.get(trip_id):
        return jsonify({'error': 'Trip with the provided ID does not exist.'}), 404

    for field in ['name', 'address', 'check_in', 'check_out', 'cost_per_night', 'trip_id']:
        if field in data:
            setattr(accommodation, field, data[field])

    db.session.commit()
    return jsonify(accommodation_schema.dump(accommodation))

# Delete an accommodation
@accom_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_accommodation(id):
    accommodation = Accommodation.query.get(id)
    if not accommodation:
        return jsonify({'error': 'Accommodation not found.'}), 404

    db.session.delete(accommodation)
    db.session.commit()
    return jsonify({'message': f'Accommodation with ID {id} deleted successfully.'})


