from extensions import ma
from marshmallow import fields
from Models.tenant_tenancy import TenantTenancy

class TenantTenancySchema(ma.SQLAlchemySchema):
    class Meta:
        model = TenantTenancy
        load_instance = False

    id = ma.auto_field()
    tenant_id = ma.auto_field(load_only=True)
    tenancy_id = ma.auto_field(load_only=True)

    # Example nested field (one-to-many or many-to-one)
    tenant = fields.Nested("TenantSchema", only=["name"])
    tenancy = fields.Nested("TenancySchema", only=["tenant_id"])

tenant_tenancy_schema = TenantTenancySchema()
tenant_tenancies_schema = TenantTenancySchema(many=True)
