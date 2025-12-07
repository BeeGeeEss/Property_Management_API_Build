from extensions import ma
from Models.tenant_tenancy import TenantTenancy

class TenantTenancySchema(ma.SQLAlchemySchema):
    class Meta:
        model = TenantTenancy
        load_instance = False

    id = ma.auto_field()
    tenant_id = ma.auto_field()
    tenancy_id = ma.auto_field()

tenant_tenancy_schema = TenantTenancySchema()
tenant_tenancies_schema = TenantTenancySchema(many=True)
