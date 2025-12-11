"""
Property Schemas

This module defines Marshmallow schemas for serializing and deserializing
Property objects. It includes:
    - PropertySchema: Basic schema for Property
    - PropertyWithManagerSchema: Nested schema including the related PropertyManager

Attributes:
    property_schema (PropertySchema): Single Property schema instance.
    properties_schema (PropertySchema): Multiple Property schema instance.
    property_with_manager_schema (PropertyWithManagerSchema): Single nested schema instance.
    properties_with_manager_schema (PropertyWithManagerSchema): Multiple nested schema instance.
"""

# Imports
from marshmallow import fields
from extensions import ma
from Models.property import Property

class PropertySchema(ma.SQLAlchemySchema):
    """
    Basic schema for Property.

    Fields:
        id (int): Primary key.
        address (str): Address of the property.
        property_manager_id (int): Foreign key to the PropertyManager (load_only).
    """
    class Meta:
        model = Property
        load_instance = False
        ordered = True

    id = ma.auto_field()
    address = ma.auto_field()
    property_manager_id = ma.auto_field(load_only=True)

class PropertyWithManagerSchema(ma.SQLAlchemySchema):
    class Meta:
        """
        Nested schema for Property including the related PropertyManager.

        Fields:
            id (int): Primary key.
            address (str): Address of the property.
            property_manager (PropertyManagerSchema): Nested PropertyManager info (id, name).
        """
        model = Property
        load_instance = True
        ordered = True

    id = ma.auto_field()
    address = ma.auto_field()
    property_manager = fields.Nested("PropertyManagerSchema", only=["id", "name"])

# Schema Instances
property_schema = PropertySchema()
properties_schema = PropertySchema(many=True)
property_with_manager_schema = PropertyWithManagerSchema()
properties_with_manager_schema = PropertyWithManagerSchema(many=True)
