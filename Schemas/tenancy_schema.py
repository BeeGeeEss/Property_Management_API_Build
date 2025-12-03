from main import ma

# create the Competition Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
class TenancySchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "start_date", "end_date", "tenancy_status", "property_id", "created_at", "updated_at")

# single competition schema, when one competition needs to be retrieved
tenancy_schema = TenancySchema()
# multiple competition schema, when many competitions need to be retrieved
tenancies_schema = TenancySchema(many=True)