from main import db
from sqlalchemy.sql import func

class TenantTenancy(db.Model):
    # define the table name for the db
    __tablename__= "tenant_tenancy"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    id = db.Column(db.Integer,primary_key=True)
    tenancy_id = db.Column(db.Integer, db.ForeignKey("tenancy.id"))
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenant.id"))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    tenancy = db.relationship("Tenancy", back_populates="tenant_links")
    tenant = db.relationship("Tenant", back_populates="tenancy_links")