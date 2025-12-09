from marshmallow import fields
from extensions import ma
from Models.support_worker import SupportWorker

class SupportWorkerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = SupportWorker
        load_instance = False
        ordered = True

    id = ma.auto_field()
    name = ma.auto_field()
    phone = ma.auto_field()
    email = ma.auto_field()

class SupportWorkerWithTenantSchema(ma.SQLAlchemySchema):
    class Meta:
        model = SupportWorker
        load_instance = False
        ordered = True

    id = ma.auto_field()
    name = ma.auto_field()
    phone = ma.auto_field()
    email = ma.auto_field()
    tenants = fields.List(fields.Nested("TenantSchema", only=["id","name"]))

support_worker_schema = SupportWorkerSchema()
support_workers_schema = SupportWorkerSchema(many=True)
support_worker_with_tenants_schema = SupportWorkerWithTenantSchema()
support_workers_with_tenants_schema = SupportWorkerWithTenantSchema(many=True)