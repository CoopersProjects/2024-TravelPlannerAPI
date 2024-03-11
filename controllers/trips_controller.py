from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from flask import Blueprint, jsonify, request
from models.trips import Trip, TripSchema
from models.destination import Destination
from models.users import User
from sqlalchemy.orm import joinedload

trip_bp = Blueprint('trips', __name__, url_prefix='/trip')

trip_schema = TripSchema()
trips_schema = TripSchema(many=True)

# Create a trip
@trip_bp.route('/create', methods=['POST'])
@jwt_required()
def create_trip():
    user_id = request.json.get('user_id')
    destination_id = request.json.get('destination_id')
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')
    budget = request.json.get('budget')

    if not all([user_id, destination_id, start_date, end_date, budget]):
        return jsonify({'error': 'Missing required fields.'}), 400

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Please provide dates in YYYY-MM-DD format.'}), 400

    if start_date >= end_date:
        return jsonify({'error': 'End date must be after start date.'}), 400

    if not (User.query.get(user_id) and Destination.query.get(destination_id)):
        return jsonify({'error': 'Invalid user_id or destination_id.'}), 400

    # Ensure budget is a float
    try:
        budget = float(budget)
    except ValueError:
        return jsonify({'error': 'Invalid budget value. Please provide a float value.'}), 400

    new_trip = Trip(user_id=user_id, destination_id=destination_id, start_date=start_date, end_date=end_date, budget=budget)

    db.session.add(new_trip)
    db.session.commit()

    trip_data = trip_schema.dump(new_trip)

    return jsonify(trip_data)

# Get all trips
@trip_bp.route('/read', methods=['GET'])
def get_trips():
    all_trips = Trip.query.all()
    result = trips_schema.dump(all_trips)
    return jsonify(result)

# Get single trip by ID
@trip_bp.route('/read/<int:id>', methods=['GET'])
def get_trip(id):
    trip = Trip.query.get(id)
    if not trip:
        return jsonify({'error': 'Trip not found.'}), 404
    trip_data = trip_schema.dump(trip)
    return jsonify(trip_data)

# Update a trip
@trip_bp.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_trip(id):
    trip = Trip.query.get(id)

    if not trip:
        return jsonify({'error': 'Trip not found.'}), 404 

    # Proceed with updating the trip
    user_id = request.json.get('user_id')
    destination_id = request.json.get('destination_id')
    start_date_str = request.json.get('start_date')
    end_date_str = request.json.get('end_date')
    budget = request.json.get('budget')

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Please provide dates in YYYY-MM-DD format.'}), 400

    if start_date >= end_date:
        return jsonify({'error': 'End date must be after start date.'}), 400

    if not (User.query.get(user_id) and Destination.query.get(destination_id)):
        return jsonify({'error': 'Invalid user_id or destination_id.'}), 400

    # Ensure budget is a float
    try:
        budget = float(budget)
    except ValueError:
        return jsonify({'error': 'Invalid budget value. Please only use numbers.'}), 400

    trip.user_id = user_id
    trip.destination_id = destination_id
    trip.start_date = start_date
    trip.end_date = end_date
    trip.budget = budget

    db.session.commit()

    trip_data = trip_schema.dump(trip)

    return jsonify(trip_data)

# Delete a trip
@trip_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_trip(id):
    trip = Trip.query.options(joinedload(Trip.destination)).get(id)

    if not trip:
        return jsonify({'error': 'Trip not found.'}), 404

    db.session.delete(trip)
    db.session.commit()

    return jsonify({'message': f'Successfully deleted trip {id}'}), 200