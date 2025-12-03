from flask import Flask
from extensions import db, ma
# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow

from dotenv import load_dotenv
load_dotenv()

from Controllers import registerable_controllers
from commands import db_commands


# creating our database object! This allows us to use our ORM
# db = SQLAlchemy()

# creating our marshmallow object! This allows us to use schemas
# ma = Marshmallow()

def create_app():
    """Docstring"""
    # Creating the flask app object - this is the core of our app!
    app = Flask(__name__)

    # configuring our app:
    app.config.from_object("config.app_config")

    # initialising our database object with the flask app
    db.init_app(app)

    # initialising our marshmallow object with the flask app
    ma.init_app(app)

    # Import the database CLI commands and register them as a blueprint.
    # This allows you to run commands like "flask db create", "flask db drop".
    app.register_blueprint(db_commands)

    # import the controllers and activate the blueprints
    for blueprint in registerable_controllers:
        app.register_blueprint(blueprint)

    # for controller in registerable_controllers:
    #     app.register_blueprint(controller)

    return app
