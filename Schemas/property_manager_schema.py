"""
PropertyManager Schemas

This module defines Marshmallow schemas for serializing and deserializing
PropertyManager objects. It includes:
    - PropertyManagerSchema: Basic schema for PropertyManager
    - PropertyManagerWithPropertiesSchema: Nested schema including related Properties

Attributes:
    property_manager_schema (PropertyManagerSchema): Single PropertyManager schema instance.
    property_managers_schema (PropertyManagerSchema): List/multiple PropertyManager schema instance.
    property_manager_with_properties_schema (PropertyManagerWithPropertiesSchema): Single nested schema.
    property_managers_with_properties_schema (PropertyManagerWithPropertiesSchema): Multiple nested schema.

"""

# Imports
from marshmallow import fields
from extensions import ma
from Models.property_manager import PropertyManager

class PropertyManagerSchema(ma.SQLAlchemySchema):
    class Meta:
        """
        Basic schema for PropertyManager.

        Fields:
            id (int): Primary key.
            name (str): Name of the property manager.
            phone (str): Phone number.
            email (str): Email address.
        """
        model = PropertyManager
        load_instance = False
        ordered = True

    id = ma.auto_field()
    name = ma.auto_field()
    phone = ma.auto_field()
    email = ma.auto_field()

class PropertyManagerWithPropertiesSchema(ma.SQLAlchemySchema):
    class Meta:
        """
        Nested schema for PropertyManager including related Properties.

        Fields:
            id (int): Primary key.
            name (str): Name of the property manager.
            phone (str): Phone number.
            email (str): Email address.
            properties (list[PropertySchema]): List of properties with limited fields (id, address).
        """
        model = PropertyManager
        load_instance = False
        ordered = True

    id = ma.auto_field()
    name = ma.auto_field()
    phone = ma.auto_field()
    email = ma.auto_field()
    properties = fields.List(fields.Nested("PropertySchema", only=["id", "address"]))

# Schema Instances
property_manager_schema = PropertyManagerSchema()
property_managers_schema = PropertyManagerSchema(many=True)
property_manager_with_properties_schema = PropertyManagerWithPropertiesSchema()
property_managers_with_properties_schema = PropertyManagerWithPropertiesSchema(many=True)
