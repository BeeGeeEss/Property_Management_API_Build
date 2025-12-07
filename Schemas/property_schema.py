from extensions import ma
from marshmallow import fields
from Models.property import Property

class PropertySchema(ma.SQLAlchemySchema):
    ordered = True
    property_manager = fields.Nested("PropertyManagerSchema", only=["id", "name"])
    class Meta:
        model = Property
        load_instance = False

    id = ma.auto_field()
    address = ma.auto_field()

    property_manager_id = ma.auto_field(load_only=True)

    # Example nested field (one-to-many or many-to-one)
    

    tenancy = fields.List(fields.Nested("TenancySchema"))

property_schema = PropertySchema()
properties_schema = PropertySchema(many=True)
