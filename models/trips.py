from init import db
from datetime import datetime
from marshmallow import Schema, fields
from models.users import User
from models.accommodation import Accommodation
from models.transportation import Transportation
from models.activities import Activity
from models.destination import Destination

# Trip Class model

class Trip(db.Model):
    __tablename__ = "trips"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    budget = db.Column(db.Float, nullable=True)  

    # Back references/backpopulates
    accommodations = db.relationship('Accommodation', backref='trip', lazy=True)
    activities = db.relationship('Activity', backref='trip', lazy=True)
    transportations = db.relationship('Transportation', backref='trip', lazy=True)
    destination = db.relationship('Destination', backref='trips', lazy=True)

    user = db.relationship('User', backref='trips', lazy=True)

    def __repr__(self):
        return f"<Trip {self.id}>"
    
# Trip model schema
class TripSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    destination_id = fields.Integer(required=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    budget = fields.Float(allow_none=True)

    accommodations = fields.Nested('AccommodationSchema', many=True)
    activities = fields.Nested('ActivitySchema', many=True)
    transportations = fields.Nested('TransportationSchema', many=True)
    destination = fields.Nested('DestinationSchema', many=False)

    accommodations = fields.Nested('AccommodationSchema', many=True)
    activities = fields.Nested('ActivitySchema', many=True)
    transportations = fields.Nested('TransportationSchema', many=True)


trip_schema = TripSchema()
trips_schema = TripSchema(many=True)