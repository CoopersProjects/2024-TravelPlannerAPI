import os

from flask import Flask
from marshmallow.exceptions import ValidationError

from init import db, ma, bcrypt, jwt

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URI")
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY")

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @app.errorhandler(400)
    def bad_request(err):
        return {"error": str(err)}, 400
    
    @app.errorhandler(404)
    def not_found(err):
        return {"error": str(err)}, 404

    @app.errorhandler(ValidationError)
    def validation_error(error):
        return {"error": error.messages}, 400
    
    # Registering controllers

    from controllers.cli_controller import db_commands
    app.register_blueprint(db_commands)

    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from controllers.trips_controller import trip_bp
    app.register_blueprint(trip_bp)

    from controllers.accommodation_controller import accom_bp
    app.register_blueprint(accom_bp)

    from controllers.transportation_controller import transport_bp
    app.register_blueprint(transport_bp)

    from controllers.activities_controller import activity_bp
    app.register_blueprint(activity_bp)

    from controllers.destination_controller import destination_bp
    app.register_blueprint(destination_bp)


    return app