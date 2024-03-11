from init import db, ma 
from marshmallow import Schema, fields

# User class creation

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
    
# User schema
    
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "email", "password")
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)

user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])