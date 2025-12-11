# Application module
from extensions import db

class TenantTenancy(db.Model):
    """
    TenantTenancy Model

    Association (junction) table representing the many-to-many relationship
    between Tenants and Tenancies in the Property Management system.

    Attributes:
        id (int): Primary key.
        rank (int, optional): Optional ranking or order for the tenant within the tenancy.
        tenancy_id (int): Foreign key linking to Tenancy.
        tenant_id (int): Foreign key linking to Tenant.
        tenancy (Tenancy): Relationship to the Tenancy model.
        tenant (Tenant): Relationship to the Tenant model.

    Relationships:
        - Many-to-many relationship between Tenant and Tenancy through this table.
        - Uses back_populates and overlaps to maintain ORM consistency.
    """
    __tablename__= "tenant_tenancy"

    id = db.Column(db.Integer,primary_key=True)
    rank = db.Column(db.Integer)
    tenancy_id = db.Column(db.Integer, db.ForeignKey("tenancy.id", ondelete="CASCADE"), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False)

    tenancy = db.relationship(
        "Tenancy",
        back_populates="tenant_tenancy",
        overlaps="tenants, tenancies"
    )
    tenant = db.relationship(
        "Tenant",
        back_populates="tenant_tenancy",
        overlaps="tenants, tenancies"
    )
