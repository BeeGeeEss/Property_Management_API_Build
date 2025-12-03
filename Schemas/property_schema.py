from main import ma

# create the Competition Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
class PropertySchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "address", "property_manager_id", "created_at", "updated_at")

# single competition schema, when one competition needs to be retrieved
property_schema = PropertySchema()
# multiple competition schema, when many competitions need to be retrieved
properties_schema = PropertySchema(many=True)