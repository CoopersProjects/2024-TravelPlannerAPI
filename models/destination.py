from init import db
from marshmallow import Schema, fields

# Destination class model

class Destination(db.Model):
    __tablename__ = "destinations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=False)
    climate_id = db.Column(db.Integer, db.ForeignKey('climates.id'), nullable=False)

    climate = db.relationship('Climate', backref='destinations', lazy=True)

    def __repr__(self):
        return f"<Destination {self.name}>"

# Destination class schema
class DestinationSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    description = fields.String()
    location = fields.String(required=True)
    climate_id = fields.Integer(required=True)

destination_schema = DestinationSchema()
destinations_schema = DestinationSchema(many=True)

