from init import db
from marshmallow import Schema, fields


class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    cost = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<Activity {self.id}>"

class ActivitySchema(Schema):
    id = fields.Integer(dump_only=True)
    trip_id = fields.Integer(required=True)
    name = fields.String(required=True)
    description = fields.String(required=False)
    cost = fields.Float(required=False)

activity_schema = ActivitySchema()
activities_schema = ActivitySchema(many=True)
