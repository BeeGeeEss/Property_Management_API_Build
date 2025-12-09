from extensions import db

class TenantTenancy(db.Model):
    # define the table name for the db
    __tablename__= "tenant_tenancy"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    id = db.Column(db.Integer,primary_key=True)
    rank = db.Column(db.Integer)
    tenancy_id = db.Column(db.Integer, db.ForeignKey("tenancy.id", ondelete="CASCADE"), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False)
    tenancy = db.relationship(
        "Tenancy",
        back_populates="tenant_tenancy"
    )
    tenant = db.relationship(
        "Tenant",
        back_populates="tenant_tenancy"
    )