"""
Main application entry point for the Property Management API.

This module:
- Loads environment variables
- Creates and configures the Flask application instance
- Initializes extensions (SQLAlchemy, Marshmallow)
- Registers CLI commands
- Registers all controller blueprints

"""

import logging
from flask import Flask, send_from_directory, jsonify
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException

# Third party extensions
from extensions import db, ma

# Application Modules
from Controllers import registerable_controllers
from commands import db_commands

# Load variables from the .env file (e.g., database credentials)
load_dotenv()

def create_app():
    """Create and configure the Flask application instance.

    Responsibilities:
        - Initialize the Flask app using the factory pattern
        - Load configuration settings (from config.app_config)
        - Initialize database and serialization extensions
        - Register CLI command blueprints
        - Register all controller blueprints for routing

    Returns:
        Flask: The fully configured Flask application instance."""
    app = Flask(__name__)

    # Load application configuration settings
    app.config.from_object("config.app_config")
    app.json.sort_keys = False

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)

    # Register custom database CLI commands (flask db create, db drop, etc.)
    app.register_blueprint(db_commands)

    @app.route("/")
    def landing_page():
        return send_from_directory("static", "index.html")

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = {
            "error": e.name,
            "description": e.description,
            "status_code": e.code
        }
        return jsonify(response), e.code

    @app.errorhandler(Exception)
    def handle_general_exception(e):
        logging.exception(e)  # logs full traceback for debugging
        response = {
            "error": "Internal Server Error",
            "description": str(e),
            "status_code": 500
        }
        return jsonify(response), 500

    # Register all API blueprints from the controllers package
    for blueprint in registerable_controllers:
        app.register_blueprint(blueprint)

    return app
