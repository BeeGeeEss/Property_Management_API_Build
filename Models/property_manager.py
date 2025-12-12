# Application module
from sqlalchemy.orm import validates
from marshmallow import ValidationError
from extensions import db

class PropertyManager(db.Model):
    """
    PropertyManager Model

    Represents a property manager in the Property Management system.

    Attributes:
        id (int): Primary key.
        name (str): Full name of the property manager.
        phone (str): Contact phone number.
        email (str): Contact email address.
        properties (list[Property]): One-to-many relationship with Property.

    Relationships:
        - One PropertyManager can manage multiple Properties.

    """
    __tablename__ = "property_manager"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    @validates("email")
    def validate_email(self, key, value):
        """
    Validates the email field for the model.

    Ensures the provided value contains an "@" symbol, indicating a minimally
    valid email format. Raises a ValidationError if validation fails.
    
    """
        if "@" not in value:
            raise ValidationError("Invalid email address")
        return value

    # One-to-many: PropertyManager -> Property
    properties = db.relationship(
        "Property",
        back_populates="property_manager",
        cascade="all, delete",
        passive_deletes=True
    )
