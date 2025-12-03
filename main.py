from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


# creating our database object! This allows us to use our ORM
db = SQLAlchemy()

# creating our marshmallow object! This allows us to use schemas
ma = Marshmallow()

def create_app():
    
    # Creating the flask app object - this is the core of our app!
    app = Flask(__name__)

    # configuring our app:
    app.config.from_object("config.app_config")

    # initialising our database object with the flask app
    db.init_app(app)

    # initialising our marshmallow object with the flask app
    ma.init_app(app)

    from commands import db_commands
    app.register_blueprint(db_commands)
    
    return app