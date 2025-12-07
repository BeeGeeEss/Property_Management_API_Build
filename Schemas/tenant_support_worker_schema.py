from extensions import ma
from Models.tenant_support_worker import TenantSupportWorker

class TenantSupportWorkerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TenantSupportWorker
        load_instance = False

    id = ma.auto_field()
    tenant_id = ma.auto_field()
    support_worker_id = ma.auto_field()

tenant_support_worker_schema = TenantSupportWorkerSchema()
tenant_support_workers_schema = TenantSupportWorkerSchema(many=True)
