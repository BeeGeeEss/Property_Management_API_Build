from extensions import ma
from Models.support_worker import SupportWorker

class SupportWorkerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = SupportWorker
        load_instance = False

    id = ma.auto_field()
    name = ma.auto_field()
    phone = ma.auto_field()
    email = ma.auto_field()

support_worker_schema = SupportWorkerSchema()
support_workers_schema = SupportWorkerSchema(many=True)