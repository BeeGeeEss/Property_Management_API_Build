from marshmallow import fields
from extensions import ma
from Models.tenant import Tenant

class TenantSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tenant
        load_instance = False
        ordered = True

    id = ma.auto_field()
    name = ma.auto_field()
    date_of_birth = ma.auto_field()
    phone = ma.auto_field()
    email = ma.auto_field()

class TenantWithTenanciesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tenant
        load_instance = False
        ordered = True

    id = ma.auto_field()
    name = ma.auto_field()
    phone = ma.auto_field()
    email = ma.auto_field()
    tenancies = fields.List(fields.Nested("TenancySchema", only=["id","start_date","end_date","tenancy_status"]))


class TenantWithSupportWorkerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tenant
        load_instance = False
        ordered = True

    id = ma.auto_field()
    name = ma.auto_field()
    phone = ma.auto_field()
    email = ma.auto_field()
    support_workers = fields.List(fields.Nested("SupportWorkerSchema", only=["id","name"]))

tenant_schema = TenantSchema()
tenants_schema = TenantSchema(many=True)
tenant_with_tenancies_schema = TenantWithTenanciesSchema()
tenants_with_tenancies_schema = TenantWithTenanciesSchema(many=True)
tenant_with_support_worker_schema = TenantWithSupportWorkerSchema()
tenants_with_support_worker_schema = TenantWithSupportWorkerSchema(many=True)