from extensions import db

class Tenancy(db.Model):
    # define the table name for the db
    __tablename__= "tenancy"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    id = db.Column(db.Integer,primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    tenancy_status = db.Column(db.String(50), nullable=False)
    
    # One-to-many backref
    property = db.relationship("Property", back_populates="tenancies")

    # Many-to-many: Tenancy <-> Tenant
    # relationship to TenantTenancy
    tenant_tenancy = db.relationship(
        "TenantTenancy",
        back_populates="tenancy",
        cascade="all, delete-orphan"
    )

    tenants = db.relationship(
        "Tenant",
        secondary="tenant_tenancy",
        back_populates="tenancies"
    )
