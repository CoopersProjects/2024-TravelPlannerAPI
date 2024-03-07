from flask import Blueprint
from init import db, bcrypt
from models.users import User
from models.accomodation import Accommodation
from models.trips import Trip


db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_tables():
    db.create_all()
    print("Tables created.")

@db_commands.cli.command('drop')
def drop_tables():
    db.drop_all()
    print("Tables dropped.")

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