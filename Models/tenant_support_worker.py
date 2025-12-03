from main import db
from sqlalchemy.sql import func

class TenantSupportWorker(db.Model):
    # define the table name for the db
    __tablename__= "tenant_support_worker"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    id = db.Column(db.Integer,primary_key=True)
    support_worker_id = db.Column(db.Integer, db.ForeignKey("support_worker.id"))
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenant.id"))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    support_worker = db.relationship("SupportWorker", back_populates="tenant_links")
    tenant = db.relationship("Tenant", back_populates="support_worker_links")