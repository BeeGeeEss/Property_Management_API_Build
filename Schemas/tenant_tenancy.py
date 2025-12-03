from extensions import ma
from Models.tenant_tenancy import TenantTenancy

class TenantTenancySchema(ma.SQLAlchemySchema):
    class Meta:
        model = TenantTenancy
        load_instance = True

    tenant_tenancy_id = ma.auto_field()
    tenant_id = ma.auto_field()
    tenancy_id = ma.auto_field()

tenant_tenancy_schema = TenantTenancySchema()
tenant_tenancies_schema = TenantTenancySchema(many=True)


# # create the Competition Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
# class TenantTenancySchema(ma.Schema):
#     class Meta:
#         # Fields to expose
#         fields = ("id", "tenant_id", "tenancy_id")

# # single competition schema, when one competition needs to be retrieved
# tenant_tenancy_schema = TenantTenancySchema()
# # multiple competition schema, when many competitions need to be retrieved
# tenant_tenancies_schema = TenantTenancySchema(many=True)