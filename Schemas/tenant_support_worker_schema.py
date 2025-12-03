from extensions import ma
from Models.tenant_support_worker import TenantSupportWorker

class TenantSupportWorkerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TenantSupportWorker
        load_instance = True

    tenant_support_worker_id = ma.auto_field()
    tenant_id = ma.auto_field()
    support_worker_id = ma.auto_field()

tenant_support_worker_schema = TenantSupportWorkerSchema()
tenant_support_workers_schema = TenantSupportWorkerSchema(many=True)


# # create the Competition Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
# class TenantSupportWorkerSchema(ma.Schema):
#     class Meta:
#         # Fields to expose
#         fields = ("id", "support_worker_id", "tenant_id")

# # single competition schema, when one competition needs to be retrieved
# tenant_support_worker_schema = TenantSupportWorkerSchema()
# # multiple competition schema, when many competitions need to be retrieved
# tenant_support_workers_schema = TenantSupportWorkerSchema(many=True)