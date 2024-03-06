from flask import Blueprint, jsonify, request
from init import db
from models.trips import Trip, TripSchema
from datetime import datetime
from models.users import User

trip_bp = Blueprint('trips', __name__, url_prefix='/trip')

trip_schema = TripSchema()
trips_schema = TripSchema(many=True)

# Create a trip
@trip_bp.route('/create', methods=['POST'])
def create_trip():
    user_id = request.json.get('user_id')
    destination_id = request.json.get('destination_id')
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')
    budget = request.json.get('budget')

    
    if not all([user_id, destination_id, start_date, end_date, budget]):
        return jsonify({'error': 'Missing required fields.'}), 400
    
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
        return jsonify({'error': 'Invalid budget value. Please provide a float value.'}), 400

    new_trip = Trip(user_id=user_id, destination_id=destination_id, start_date=start_date, end_date=end_date, budget=budget)

    db.session.add(new_trip)
    db.session.commit()

    return trip_schema.jsonify(new_trip)

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
    return trip_schema.jsonify(trip)

# Update a trip
@trip_bp.route('/update/<int:id>', methods=['PUT'])
def update_trip(id):
    trip = Trip.query.get(id)

    if not trip:
        return jsonify({'error': 'Trip not found.'}), 404 

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
        return jsonify({'error': 'Invalid budget value. Please provide a float value.'}), 400

    trip.user_id = user_id
    trip.destination_id = destination_id
    trip.start_date = start_date
    trip.end_date = end_date
    trip.budget = budget

    db.session.commit()

    return trip_schema.jsonify(trip)

# Delete a trip
@trip_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_trip(id):
    trip = Trip.query.get(id)

    if not trip:
        return jsonify({'error': 'Trip not found.'}), 404

    db.session.delete(trip)
    db.session.commit()

    return trip_schema.jsonify(trip)
