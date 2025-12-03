from extensions import ma
from Models.property_manager import PropertyManager

class PropertyManagerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PropertyManager
        load_instance = True

    id = ma.auto_field()
    name = ma.auto_field()
    phone = ma.auto_field()
    email = ma.auto_field()

property_manager_schema = PropertyManagerSchema()
property_managers_schema = PropertyManagerSchema(many=True)

# # create the Competition Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
# class PropertyManagerSchema(ma.Schema):
#     class Meta:
#         # Fields to expose
#         fields = ("id", "name", "phone", "email")

# # single competition schema, when one competition needs to be retrieved
# property_manager_schema = PropertyManagerSchema()
# # multiple competition schema, when many competitions need to be retrieved
# property_managers_schema = PropertyManagerSchema(many=True)