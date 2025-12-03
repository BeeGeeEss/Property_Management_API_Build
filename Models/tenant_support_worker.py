from main import db

class TenantSupportWorker(db.Model):
    # define the table name for the db
    __tablename__= "tenant_support_worker"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    id = db.Column(db.Integer,primary_key=True)
    support_worker_id = db.Column(db.Integer, db.ForeignKey("support_worker.id"))
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenant.id"))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    tenant = db.relationship("tenant", back_populates="tenant_support_worker")
    support_worker = db.relationship("support_worker", back_populates="tenant_support_worker")