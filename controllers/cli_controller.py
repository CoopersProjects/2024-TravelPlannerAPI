from datetime import date

from flask import Blueprint
from sqlalchemy import inspect
from init import db, bcrypt

from models.users import User
from models.accommodation import Accommodation
from models.trips import Trip
from models.activities import Activity
from models.destination import Destination
from models.transportation import Transportation
from models.climate import Climate
from models.transportType import TransportType

db_commands = Blueprint('db', __name__)

# Create database tables
@db_commands.cli.command('create')
def create_tables():
    table_creation_order = [User, Climate, Destination, Trip, Accommodation, Activity, TransportType, Transportation]
    inspector = inspect(db.engine)
    
    for model in table_creation_order:
        table_name = model.__table__.name
        if table_name not in inspector.get_table_names():
            model.__table__.create(db.engine)
            print(f"Table {table_name} created.")
        else:
            print(f"Table {table_name} already exists.")
# Drop database tables
@db_commands.cli.command('drop')
def drop_tables():
    db.drop_all()
    print("Tables dropped.")
# Seed database tables
@db_commands.cli.command('seed')
def seed_tables():
   users = [
       User(
           username="User1",
           email="user1@email.com",
           password=bcrypt.generate_password_hash('123456').decode('utf-8')
       ),
       User(
           username="User2",
           email="user2@email.com",
           password=bcrypt.generate_password_hash('123456').decode('utf-8')
       )
   ]

   db.session.add_all(users)

   
   db.session.commit()

   print("Tables seeded.")