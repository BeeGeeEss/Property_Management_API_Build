"""
Configuration settings for the Flask application.

Provides different configurations for:
- Development
- Production
- Testing

"""

# Standard library imports
import os

class Config(object):
    """
    Base configuration class.

    Provides access to environment variables and default settings
    common to all environments.
    """
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        """
        Return the SQLAlchemy database URI from environment variables.

        Raises:
            ValueError: If DATABASE_URL is not set in environment variables.
        """
        # access to .env and get the value of DATABASE_URL, the variable name can be any but needs to match
        value = os.environ.get("DATABASE_URL")
        if not value:
            raise ValueError("DATABASE_URL is not set")
        return value

class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production environment configuration."""
    pass

class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True

# Determine which configuration to use based on FLASK_ENV environment variable
environment = os.environ.get("FLASK_ENV")
if environment == "production":
    app_config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
else:
    app_config = DevelopmentConfig()
