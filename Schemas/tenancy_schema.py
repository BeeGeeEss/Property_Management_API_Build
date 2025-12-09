from marshmallow import fields
from extensions import ma
from Models.tenancy import Tenancy

class TenancySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tenancy
        load_instance = False
        ordered = True

    id = ma.auto_field()
    start_date = ma.auto_field()
    end_date = ma.auto_field()
    tenancy_status = ma.auto_field()
    property_id = ma.auto_field(load_only=True)

class TenancyWithPropertySchema(TenancySchema):
    model = Tenancy
    load_instance = True

    id = ma.auto_field()
    property = fields.Nested("PropertySchema", only=["id", "address"])


class TenancyWithTenantsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tenancy
        load_instance = False
        ordered = True

    id = ma.auto_field()
    start_date = ma.auto_field()
    end_date = ma.auto_field()
    tenancy_status = ma.auto_field()
    tenants = fields.List(fields.Nested("TenantSchema", only=["id", "name"]))

tenancy_schema = TenancySchema()
tenancies_schema = TenancySchema(many=True)
tenancy_with_property_schema = TenancyWithPropertySchema()
tenancies_with_property_schema = TenancyWithPropertySchema(many=True)
tenancy_with_tenants_schema = TenancyWithTenantsSchema()
tenancies_with_tenants_schema =TenancyWithTenantsSchema(many=True)
