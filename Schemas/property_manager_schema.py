from extensions import ma
from Models.property_manager import PropertyManager

class PropertyManagerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PropertyManager
        load_instance = False

    id = ma.auto_field()
    name = ma.auto_field()
    phone = ma.auto_field()
    email = ma.auto_field()

property_manager_schema = PropertyManagerSchema()
property_managers_schema = PropertyManagerSchema(many=True)
