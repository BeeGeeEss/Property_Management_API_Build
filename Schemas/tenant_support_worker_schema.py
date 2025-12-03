from main import ma

# create the Competition Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
class TenantSupportWorkerSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "support_worker_id", "tenant_id", "created_at", "updated_at")

# single competition schema, when one competition needs to be retrieved
tenant_support_worker_schema = TenantSupportWorkerSchema()
# multiple competition schema, when many competitions need to be retrieved
tenant_support_workers_schema = TenantSupportWorkerSchema(many=True)