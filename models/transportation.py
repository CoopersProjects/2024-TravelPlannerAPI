from init import db
from marshmallow import Schema, fields
from models.transportType import TransportType  

class Transportation(db.Model):
    __tablename__ = "transportations"

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    transport_type_id = db.Column(db.Integer, db.ForeignKey('transport_types.id'), nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_location = db.Column(db.String(100), nullable=False)
    departure_location = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Float, nullable=False)

    transport_type = db.relationship('TransportType', backref='transportations', lazy=True)

    def __repr__(self):
        return f"<Transportation {self.id}>"

class TransportationSchema(Schema):
    id = fields.Integer(dump_only=True)
    trip_id = fields.Integer(required=True)
    transport_type_id = fields.Integer(required=True)
    arrival_time = fields.DateTime(required=True)
    departure_time = fields.DateTime(required=True)
    arrival_location = fields.String(required=True)
    departure_location = fields.String(required=True)
    cost = fields.Float(required=True)

transportation_schema = TransportationSchema()
transportations_schema = TransportationSchema(many=True)
