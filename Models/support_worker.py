from main import db
from sqlalchemy.sql import func

class SupportWorker(db.Model):
    # define the table name for the db
    __tablename__= "support_worker"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
    # Many-to-many via TenantSupportWorker
    tenant_links = db.relationship("TenantSupportWorker", back_populates="support_worker")