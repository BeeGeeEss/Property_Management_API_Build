from extensions import db

class TenantSupportWorker(db.Model):
    # define the table name for the db
    __tablename__= "tenant_support_worker"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    tenancy_support_worker_id = db.Column(db.Integer,primary_key=True)
    support_worker_id = db.Column(db.Integer, db.ForeignKey("support_worker.support_worker_id"))
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenant.tenant_id"))
