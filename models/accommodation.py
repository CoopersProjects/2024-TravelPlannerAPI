from init import db
from marshmallow import Schema, fields

# Accommodation class model

class Accommodation(db.Model):
    __tablename__ = "accommodations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    check_in = db.Column(db.DateTime, nullable=True)
    check_out = db.Column(db.DateTime, nullable=True)
    cost_per_night = db.Column(db.Float, nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)

    def __repr__(self):
        return f"<Accommodation {self.id}: {self.name}>"
    
# Accommodation class Schema
    
class AccommodationSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    address = fields.String(required=True)
    check_in = fields.DateTime(format='%Y-%m-%d')
    check_out = fields.DateTime(format='%Y-%m-%d')
    cost_per_night = fields.Float(required=True)
    trip_id = fields.Integer(required=True)

accommodation_schema = AccommodationSchema()
accommodations_schema = AccommodationSchema(many=True)