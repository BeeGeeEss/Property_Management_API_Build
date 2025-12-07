from extensions import ma
from Models.tenant import Tenant

class TenantSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tenant
        load_instance = False

    id = ma.auto_field()
    name = ma.auto_field()
    date_of_birth = ma.auto_field()
    phone = ma.auto_field()
    email = ma.auto_field()

tenant_schema = TenantSchema()
tenants_schema = TenantSchema(many=True)
