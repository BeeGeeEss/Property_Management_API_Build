from extensions import ma
from marshmallow import fields
from Models.tenant_support_worker import TenantSupportWorker

class TenantSupportWorkerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TenantSupportWorker
        load_instance = False

    id = ma.auto_field()
    tenant_id = ma.auto_field(load_only=True)
    support_worker_id = ma.auto_field(load_only=True)

    # Example nested field (one-to-many or many-to-one)
    tenant = fields.Nested("TenantSchema", only=["name"])
    support_worker = fields.Nested("SupportWorkerSchema", only=["name"])


tenant_support_worker_schema = TenantSupportWorkerSchema()
tenant_support_workers_schema = TenantSupportWorkerSchema(many=True)
