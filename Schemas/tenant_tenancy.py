from main import ma

# create the Competition Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
class TenantTenancySchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "tenant_id", "tenancy_id", "created_at", "updated_at")

# single competition schema, when one competition needs to be retrieved
tenant_tenancy_schema = TenantTenancySchema()
# multiple competition schema, when many competitions need to be retrieved
tenant_tenancies_schema = TenantTenancySchema(many=True)