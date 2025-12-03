from main import ma

# create the Competition Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
class TenantSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "date_of_birth", "name", "phone", "email", "created_at", "updated_at")

# single competition schema, when one competition needs to be retrieved
tenant_schema = TenantSchema()
# multiple competition schema, when many competitions need to be retrieved
tenants_schema = TenantSchema(many=True)