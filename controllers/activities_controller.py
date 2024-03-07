from flask import Blueprint, jsonify, request
from init import db
from models.activities import Activity, ActivitySchema
from datetime import datetime

activity_bp = Blueprint('activity_controller', __name__, url_prefix='/activity')

activity_schema = ActivitySchema()
activities_schema = ActivitySchema(many=True)

# Create an activity
@activity_bp.route('/create', methods=['POST'])
def create_activity():
    trip_id = request.json.get('trip_id')
    name = request.json.get('name')
    description = request.json.get('description')
    cost = request.json.get('cost')

    if not all([trip_id, name]):
        return jsonify({'error': 'Missing required fields.'}), 400
    
    # Create a new activity instance
    new_activity = Activity(trip_id=trip_id, name=name, description=description, cost=cost)

    # Add the new activity to the database
    db.session.add(new_activity)
    db.session.commit()

    # Serialize and return the new activity
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
    return activity_schema.jsonify(activity)

# Update an activity
@activity_bp.route('/update/<int:id>', methods=['PUT'])
def update_activity(id):
    activity = Activity.query.get(id)

    trip_id = request.json.get('trip_id')
    name = request.json.get('name')
    description = request.json.get('description')
    cost = request.json.get('cost')

    if not activity:
        return jsonify({'error': 'Activity not found.'}), 404 

    activity.trip_id = trip_id
    activity.name = name
    activity.description = description
    activity.cost = cost

    db.session.commit()

    return activity_schema.jsonify(activity)

# Delete an activity
@activity_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_activity(id):
    activity = Activity.query.get(id)

    if not activity:
        return jsonify({'error': 'Activity not found.'}), 404  
    
    db.session.delete(activity)
    db.session.commit()

    return activity_schema.jsonify(activity)
