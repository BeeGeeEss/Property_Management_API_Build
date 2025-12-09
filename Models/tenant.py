from extensions import db

class Tenant(db.Model):
    # define the table name for the db
    __tablename__= "tenant"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(50))

    # relationship to TenantTenancy
    tenant_tenancy = db.relationship(
        "TenantTenancy",
        back_populates="tenant",
        cascade="all, delete-orphan"
    )
    
    # relationship to TenantSupportWorker
    tenant_support_worker = db.relationship(
        "TenantSupportWorker",
        back_populates="tenant",
        cascade="all, delete-orphan"
    )

    tenancies = db.relationship(
        "Tenancy",
        secondary="tenant_tenancy",
        back_populates="tenants",
        overlaps="tenant_tenancy"
    )

    support_workers = db.relationship(
    "SupportWorker",
    secondary="tenant_support_worker",
    back_populates="tenants",
    overlaps="tenant_support_worker"
    )