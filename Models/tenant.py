# Application module
from extensions import db

class Tenant(db.Model):
    """
    Tenant Model

    Represents a tenant in the Property Management system.

    Attributes:
        id (int): Primary key.
        name (str): Full name of the tenant.
        date_of_birth (date): Tenant's date of birth.
        phone (str, optional): Contact phone number.
        email (str, optional): Contact email address.
        tenant_tenancy (list[TenantTenancy]): Association table for many-to-many with Tenancy.
        tenant_support_worker (list[TenantSupportWorker]): Association table for many-to-many with SupportWorker.
        tenancies (list[Tenancy]): Many-to-many relationship to Tenancy through TenantTenancy.
        support_workers (list[SupportWorker]): Many-to-many relationship to SupportWorker through TenantSupportWorker.

    Relationships:
        - A Tenant can be linked to multiple Tenancies via TenantTenancy.
        - A Tenant can be linked to multiple SupportWorkers via TenantSupportWorker.
    """
    __tablename__= "tenant"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(50))

    # One-to-many: Tenant -> TenantTenancy
    tenant_tenancy = db.relationship(
        "TenantTenancy",
        back_populates="tenant",
        cascade="all, delete-orphan"
    )

    # One-to-many: Tenant -> TenantSupportWorker
    tenant_support_worker = db.relationship(
        "TenantSupportWorker",
        back_populates="tenant",
        cascade="all, delete-orphan"
    )

    # Many-to-many: Tenant <-> Tenancy through TenantTenancy
    tenancies = db.relationship(
        "Tenancy",
        secondary="tenant_tenancy",
        back_populates="tenants",
        overlaps="tenant_tenancy"
    )

    # Many-to-many: Tenant <-> SupportWorker through TenantSupportWorker
    support_workers = db.relationship(
    "SupportWorker",
    secondary="tenant_support_worker",
    back_populates="tenants",
    overlaps="tenant_support_worker"
    )
