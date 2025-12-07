from extensions import ma
from Models.property import Property

class PropertySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Property
        load_instance = False

    id = ma.auto_field()
    property_manager_id = ma.auto_field()
    address = ma.auto_field()

property_schema = PropertySchema()
properties_schema = PropertySchema(many=True)
