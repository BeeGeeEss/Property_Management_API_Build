from marshmallow import fields
from extensions import ma
from Models.property_manager import PropertyManager

class PropertyManagerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PropertyManager
        load_instance = False
        ordered = True

    id = ma.auto_field()
    name = ma.auto_field()
    phone = ma.auto_field()
    email = ma.auto_field()

class PropertyManagerWithPropertiesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PropertyManager
        load_instance = False
        ordered = True

    id = ma.auto_field()
    name = ma.auto_field()
    phone = ma.auto_field()
    email = ma.auto_field()
    properties = fields.List(fields.Nested("PropertySchema", only=["id", "address"]))

property_manager_schema = PropertyManagerSchema()
property_managers_schema = PropertyManagerSchema(many=True)
property_manager_with_properties_schema = PropertyManagerWithPropertiesSchema()
property_managers_with_properties_schema = PropertyManagerWithPropertiesSchema(many=True)