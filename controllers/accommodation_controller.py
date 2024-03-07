from flask import Blueprint, jsonify, request
from init import db
from models.accomodation import Accommodation, AccommodationSchema
from datetime import datetime

accom_bp = Blueprint('accommodation_controller', __name__, url_prefix='/accommodation')

accommodation_schema = AccommodationSchema()
accommodations_schema = AccommodationSchema(many=True)

# Create an accommodation associated with a trip
@accom_bp.route('/create', methods=['POST'])
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

    return accommodation_schema.jsonify(new_accommodation)

@accom_bp.route('/read', methods=['GET'])
def get_all_accommodations():
    accommodations = Accommodation.query.all()
    return accommodations_schema.jsonify(accommodations)

# Get accommodation by ID
@accom_bp.route('/<int:id>', methods=['GET'])
def get_accommodation(id):
    accommodation = Accommodation.query.get(id)
    if not accommodation:
        return jsonify({'error': 'Accommodation not found.'}), 404
    return accommodation_schema.jsonify(accommodation)

# Update an accommodation
@accom_bp.route('/update/<int:id>', methods=['PUT'])
def update_accommodation(id):
    accommodation = Accommodation.query.get(id)
    if not accommodation:
        return jsonify({'error': 'Accommodation not found.'}), 404

    data = request.json
    for field in ['name', 'address', 'check_in', 'check_out', 'cost_per_night', 'trip_id']:
        if field in data:
            setattr(accommodation, field, data[field])

    db.session.commit()
    return accommodation_schema.jsonify(accommodation)

# Delete an accommodation
@accom_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_accommodation(id):
    accommodation = Accommodation.query.get(id)
    if not accommodation:
        return jsonify({'error': 'Accommodation not found.'}), 404

    db.session.delete(accommodation)
    db.session.commit()
    return jsonify({'message': 'Accommodation deleted successfully.'})


