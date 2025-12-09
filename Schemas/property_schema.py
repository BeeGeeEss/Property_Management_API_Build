from marshmallow import fields
from extensions import ma
from Models.property import Property

class PropertySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Property
        load_instance = False
        ordered = True

    id = ma.auto_field()
    address = ma.auto_field()
    property_manager_id = ma.auto_field(load_only=True)

class PropertyWithManagerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Property
        load_instance = True
        ordered = True

    id = ma.auto_field()
    address = ma.auto_field()
    property_manager = fields.Nested("PropertyManagerSchema", only=["id", "name"])

property_schema = PropertySchema()
properties_schema = PropertySchema(many=True)
property_with_manager_schema = PropertyWithManagerSchema()
properties_with_manager_schema = PropertyWithManagerSchema(many=True)
