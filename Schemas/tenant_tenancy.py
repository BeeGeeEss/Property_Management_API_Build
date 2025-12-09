from marshmallow import fields
from extensions import ma
from Models.tenant_tenancy import TenantTenancy

class TenantTenancySchema(ma.SQLAlchemySchema):
    class Meta:
        model = TenantTenancy
        load_instance = False
        ordered = True

    id = ma.auto_field()
    tenant_id = ma.auto_field(load_only=True)
    tenancy_id = ma.auto_field(load_only=True)

    # Example nested field (one-to-many or many-to-one)
    tenant = fields.Nested("TenantSchema", only=["id", "name"])
    tenancy = fields.Nested("TenancySchema", only=["id", "tenancy_status"])

tenant_tenancy_schema = TenantTenancySchema()
tenant_tenancies_schema = TenantTenancySchema(many=True)
