from extensions import ma
from Models.property import Property

class PropertySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Property
        load_instance = True

    id = ma.auto_field()
    property_manager_id = ma.auto_field()
    address = ma.auto_field()

property_schema = PropertySchema()
properties_schema = PropertySchema(many=True)


# # create the Competition Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
# class PropertySchema(ma.Schema):
#     class Meta:
#         # Fields to expose
#         fields = ("id", "address", "property_manager_id")

# # single competition schema, when one competition needs to be retrieved
# property_schema = PropertySchema()
# # multiple competition schema, when many competitions need to be retrieved
# properties_schema = PropertySchema(many=True)