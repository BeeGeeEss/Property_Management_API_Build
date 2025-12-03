from main import ma

# create the Competition Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
class PropertyManagerSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name", "phone", "email", "created_at", "updated_at")

# single competition schema, when one competition needs to be retrieved
property_manager_schema = PropertyManagerSchema()
# multiple competition schema, when many competitions need to be retrieved
property_manager_schema = PropertyManagerSchema(many=True)