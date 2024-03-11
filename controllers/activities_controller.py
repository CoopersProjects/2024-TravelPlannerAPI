from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from init import db
from models.activities import Activity, ActivitySchema
from models.trips import Trip
from datetime import datetime

activity_bp = Blueprint('activity_controller', __name__, url_prefix='/activity')

activity_schema = ActivitySchema()
activities_schema = ActivitySchema(many=True)

# Create an activity
@activity_bp.route('/create', methods=['POST'])
@jwt_required()
def create_activity():
    trip_id = request.json.get('trip_id')

    # Check if the trip_id exists
    if not Trip.query.get(trip_id):
        return jsonify({'error': 'Trip not found.'}), 404

    name = request.json.get('name')
    description = request.json.get('description')
    cost = request.json.get('cost')

    if not all([trip_id, name]):
        return jsonify({'error': 'Missing required fields.'}), 400
    
    try:
        cost = float(cost)
    except ValueError:
        return jsonify({'error': 'Invalid cost value. Please provide a float value.'}), 400
    
    # Create a new activity instance
    new_activity = Activity(trip_id=trip_id, name=name, description=description, cost=cost)

    # Add the new activity to the database
    db.session.add(new_activity)
    db.session.commit()

    # Serialise and return the new activity
    return activity_schema.jsonify(new_activity)

# Get all activities
@activity_bp.route('/read', methods=['GET'])
def get_activities():
    all_activities = Activity.query.all()
    result = activities_schema.dump(all_activities)
    return jsonify(result)

# Get a single activity by ID
@activity_bp.route('/read/<int:id>', methods=['GET'])
def get_activity(id):
    activity = Activity.query.get(id)
    if not activity:
        return jsonify({'error': 'Activity not found.'}), 404
    
    activity_data = activity_schema.dump(activity)
    return jsonify(activity_data)

# Update an activity
@activity_bp.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_activity(id):
    activity = Activity.query.get(id)
    if not activity:
        return jsonify({'error': 'Activity not found.'}), 404 

    trip_id = request.json.get('trip_id')

    # Check if the trip_id exists
    if not Trip.query.get(trip_id):
        return jsonify({'error': 'Trip not found.'}), 404
    
    try:
        cost = float(cost)
    except ValueError:
        return jsonify({'error': 'Invalid cost value. Please provide a float value.'}), 400

    name = request.json.get('name')
    description = request.json.get('description')
    cost = request.json.get('cost')

    activity.trip_id = trip_id
    activity.name = name
    activity.description = description
    activity.cost = cost

    db.session.commit()

    return activity_schema.jsonify(activity)

# Delete an activity
@activity_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_activity(id):
    activity = Activity.query.get(id)

    if not activity:
        return jsonify({'error': 'Activity not found.'}), 404

    db.session.delete(activity)
    db.session.commit()

    return jsonify({'message': 'Activity deleted successfully.'})
