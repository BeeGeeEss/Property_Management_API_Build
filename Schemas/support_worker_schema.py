from main import ma

# create the Competition Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
class SupportWorkerSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name", "phone", "email", "created_at", "updated_at")

# single competition schema, when one competition needs to be retrieved
support_worker_schema = SupportWorkerSchema()
# multiple competition schema, when many competitions need to be retrieved
support_workers_schema = SupportWorkerSchema(many=True)