"""
This module initializes Flask extensions used throughout the application.
Extensions are instantiated here and later initialized with the Flask app.
"""

# Standard / third-party imports
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Flask extensions
db = SQLAlchemy()         # SQLAlchemy instance for database ORM
ma = Marshmallow()        # Marshmallow instance for object serialization/deserialization
