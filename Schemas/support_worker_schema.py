from extensions import ma
from Models.support_worker import SupportWorker

class SupportWorkerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = SupportWorker
        load_instance = True

    support_worker_id = ma.auto_field()
    name = ma.auto_field()
    phone = ma.auto_field()
    email = ma.auto_field()

support_worker_schema = SupportWorkerSchema()
support_workers_schema = SupportWorkerSchema(many=True)


# # create the Competition Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
# class SupportWorkerSchema(ma.Schema):
#     class Meta:
#         # Fields to expose
#         fields = ("id", "name", "phone", "email")

# # single competition schema, when one competition needs to be retrieved
# support_worker_schema = SupportWorkerSchema()
# # multiple competition schema, when many competitions need to be retrieved
# support_workers_schema = SupportWorkerSchema(many=True)