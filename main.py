from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# creating our database object! This allows us to use our ORM
db = SQLAlchemy()

def create_app():
    
    # Creating the flask app object - this is the core of our app!
    app = Flask(__name__)

    # configuring our app:
    app.config.from_object("config.app_config")

    # initialising our database object with the flask app
    db.init_app(app)
    
    return app